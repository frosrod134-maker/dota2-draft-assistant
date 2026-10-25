"""
Mathematical Recommendation Engine for Dota 2 Drafting (Patch 7.41f).
Features:
- Strict Role Viability Filter (No support as carry, no carry as support).
- Accurate Counter Matrix & Mechanical Archetype Multipliers.
- Smart Team Composition Awareness (penalizes double hard carry, rewards filling missing roles).
- Guaranteed non-empty category pools (Meta, Situational, Hybrid).
- Rich Russian tactical reasoning (15-25+ words) for every card.
"""

import logging
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from database.models import Hero, RoleStat, Matchup
from services.aliases import HERO_BY_ID, HERO_LIST
from services.hero_roles import HERO_VIABLE_ROLES, HERO_PRIMARY_ROLE, HARD_CARRIES
from services.hero_guides import get_mechanical_counter_multiplier, get_team_counter_items, generate_tactical_reason
from services.hero_builds import get_hero_core_items, get_situational_items_for_hero_vs_enemies
from services.hero_signatures import HERO_SIGNATURES

logger = logging.getLogger("draft_engine")

ROLE_NAMES_RU = {
    1: "Керри (Поз 1)",
    2: "Мид (Поз 2)",
    3: "Оффлейн (Поз 3)",
    4: "Семи-саппорт (Поз 4)",
    5: "Фулл-саппорт (Поз 5)",
}

SUPPORT_ROLES = {4, 5}
CORE_ROLES = {1, 2, 3}

LANE_DOMINATORS_BY_ROLE = {
    1: [70, 93, 59, 10, 1, 61, 82, 12, 4, 95, 8, 44],
    2: [59, 82, 34, 47, 65, 61, 80, 76, 17, 13, 11, 25, 39],
    3: [2, 98, 99, 36, 15, 137, 55, 28, 96, 129, 104, 29],
    4: [88, 71, 7, 51, 62, 100, 86, 136, 26, 123, 107],
    5: [85, 3, 83, 66, 79, 111, 87, 64, 30, 31, 37, 50],
}
GLOBAL_LANE_DOMINATORS = [61, 82, 59, 34, 47, 2, 98, 93, 70, 88, 85, 1, 137, 7, 12, 104]

# High-precision curated matchup advantages: (Candidate, Enemy) -> Advantage %
# Positive = Candidate counters Enemy. Negative = Candidate is countered by Enemy.
CURATED_MATCHUPS: dict[tuple[int, int], float] = {
    # ── Against Phantom Lancer (12) ──
    (7, 12): 8.5,     # Earthshaker counters PL (Echo Slam)
    (52, 12): 7.8,    # Leshrac counters PL (Pulse Nova)
    (18, 12): 7.5,    # Sven counters PL (Great Cleave)
    (72, 12): 7.2,    # Gyrocopter counters PL (Flak Cannon)
    (2, 12): 7.2,     # Axe counters PL (Call + Helix)
    (48, 12): 7.0,    # Luna counters PL (Moon Glaives)
    (89, 12): 6.8,    # Naga Siren counters PL (Rip Tide)
    (16, 12): 6.8,    # Sand King counters PL (Epicenter / Sand Storm)
    (138, 12): 6.6,   # Muerta counters PL (Pierce the Veil / Calling)
    (106, 12): 6.5,   # Ember Spirit counters PL (Sleight of Fist)
    (98, 12): 6.2,    # Timbersaw counters PL (Pure Chakram)
    (99, 12): 5.8,    # Bristleback counters PL (Quill Spray)
    # Heroes PL counters (negative for them against PL):
    (42, 12): -6.5,   # Wraith King is countered by PL
    (47, 12): -5.8,   # Viper is countered by PL
    (94, 12): -7.0,   # Medusa is countered by PL
    (1, 12): -5.5,    # Anti-Mage is countered by PL
    (6, 12): -6.0,    # Drow Ranger is countered by PL
    (35, 12): -5.8,   # Sniper is countered by PL

    # ── Against Huskar (59) ──
    (68, 59): 9.0,    # Ancient Apparition counters Huskar (Ice Blast stops heal)
    (36, 59): 7.8,    # Necrophos counters Huskar (Reaper's Scythe execute)
    (47, 59): 7.2,    # Viper counters Huskar (Nethertoxin Break)
    (25, 59): 6.8,    # Lina counters Huskar (Pure Laguna Blade burst)
    (21, 59): 6.2,    # Windranger counters Huskar (Windrun + Shackle)
    (33, 59): 5.8,    # Enigma counters Huskar (Midnight Pulse % HP)
    (98, 59): 5.5,    # Timbersaw counters Huskar (Pure damage)
    # Heroes Huskar counters:
    (46, 59): -6.5,   # Templar Assassin is countered by Huskar
    (49, 59): -5.8,   # Dragon Knight is countered by Huskar
    (22, 59): -6.2,   # Zeus is countered by Huskar
    (23, 59): -5.5,   # Kunkka is countered by Huskar

    # ── Against Anti-Mage (1) ──
    (44, 1): 7.8,     # Phantom Assassin counters AM (Physical Coup de Grace)
    (104, 1): 7.5,    # Legion Commander counters AM (Duel through Counterspell)
    (2, 1): 7.2,      # Axe counters AM (Call through Counterspell)
    (28, 1): 6.8,     # Slardar counters AM (Corrosive Haze + Bash)
    (82, 1): 6.5,     # Meepo counters AM (Earthbind root stops Blink)
    (95, 1): 6.2,     # Troll Warlord counters AM (Root/bash)
    (93, 1): 5.8,     # Slark counters AM (Pounce leash)
    (4, 1): 5.5,      # Bloodseeker counters AM (Rupture stops Blink)
    (71, 1): 5.2,     # Spirit Breaker counters AM (Charge vision + BKB bash)
    # Heroes AM counters:
    (94, 1): -7.5,    # Medusa is countered by AM
    (17, 1): -6.8,    # Storm Spirit is countered by AM
    (22, 1): -7.0,    # Zeus is countered by AM
    (52, 1): -6.5,    # Leshrac is countered by AM
    (76, 1): -6.0,    # Outworld Destroyer is countered by AM
    (34, 1): -5.5,    # Tinker is countered by AM
    (74, 1): -5.0,    # Invoker is countered by AM

    # ── Against Meepo (82) ──
    (112, 82): 8.5,   # Winter Wyvern counters Meepo
    (7, 82): 8.0,     # Earthshaker counters Meepo
    (103, 82): 7.5,   # Elder Titan counters Meepo
    (18, 82): 6.8,    # Sven counters Meepo
    (52, 82): 6.5,    # Leshrac counters Meepo

    # ── Against Morphling (10) ──
    (68, 10): 8.5,    # AA counters Morphling
    (76, 10): 6.8,    # OD counters Morphling
    (26, 10): 6.0,    # Lion counters Morphling

    # ── Against Bristleback (99) ──
    (47, 99): 8.0,    # Viper counters Bristleback
    (98, 99): 7.5,    # Timbersaw counters Bristleback
    (104, 99): 6.5,   # Legion Commander counters Bristleback
    (36, 99): 6.2,    # Necrophos counters Bristleback

    # ── Against Slark (93) ──
    (4, 93): 8.0,     # Bloodseeker counters Slark
    (87, 93): 7.0,    # Disruptor counters Slark
    (52, 93): 6.5,    # Leshrac counters Slark
    (2, 93): 6.0,     # Axe counters Slark

    # ── Against Drow Ranger (6) & Sniper (35) ──
    (71, 6): 7.5,     # Spirit Breaker counters Drow
    (51, 6): 7.2,     # Clockwerk counters Drow
    (67, 6): 7.0,     # Spectre counters Drow
    (17, 6): 6.8,     # Storm Spirit counters Drow
    (44, 6): 6.5,     # PA counters Drow
    (71, 35): 7.8,    # Spirit Breaker counters Sniper
    (51, 35): 7.5,    # Clockwerk counters Sniper
    (67, 35): 7.2,    # Spectre counters Sniper
    (14, 35): 6.5,    # Pudge counters Sniper
    (17, 35): 7.0,    # Storm counters Sniper

    # ── Against Pudge (14) ──
    (54, 14): 7.5,    # Lifestealer counters Pudge
    (70, 14): 7.0,    # Ursa counters Pudge
    (98, 14): 6.5,    # Timbersaw counters Pudge
    (36, 14): 6.0,    # Necrophos counters Pudge

    # ── Against Tinker (34) (Dotabuff counters & favorable matchups) ──
    (34, 17): -5.2,   # Storm Spirit counters Tinker (Ball Lightning into trees)
    (34, 67): -4.9,   # Spectre counters Tinker (Shadow Step / Haunt global catch)
    (34, 51): -4.8,   # Clockwerk counters Tinker (Rocket Flare vision + Hookshot)
    (34, 88): -4.6,   # Nyx Assassin counters Tinker (Spiked Carapace on March + Vendetta)
    (34, 22): -4.5,   # Zeus counters Tinker (Nimbus + Thundergod's Wrath vision)
    (34, 71): -4.2,   # Spirit Breaker counters Tinker (Charge of Darkness through trees)
    (34, 60): -4.1,   # Night Stalker counters Tinker (Dark Ascension flying vision + Crippling Fear)
    (34, 45): -3.8,   # Pugna counters Tinker (Nether Ward punishes high mana Rearm spells)
    (34, 12): 3.9,    # Tinker counters Phantom Lancer (March of the Machines + Laser blind)
    (34, 44): 3.6,    # Tinker counters Phantom Assassin (100% miss Laser + magic burst)
    (34, 109): 3.5,   # Tinker counters Terrorblade (Laser blind + magic damage)
    (34, 95): 3.3,    # Tinker counters Troll Warlord (Laser 100% miss + Defense Matrix kite)
}


class DraftCalculator:
    """
    Mathematical Recommendation Engine with Strict Role Filters & Composition Awareness:
    - 🔥 hybrid: High patch meta AND high counter advantage
    - ⚡ situational: Sharp counter-pick against enemies (or lane bully if no enemies)
    - 👑 meta: High-winrate patch comfort pick
    """

    @staticmethod
    def normalize_score(val: float, min_val: float = 0.0, max_val: float = 100.0) -> float:
        return max(min_val, min(max_val, round(val, 1)))

    async def recommend(
        self,
        db_session: AsyncSession,
        ally_ids: list[int],
        enemy_ids: list[int],
        role: int | None = None,
        top_k: int = 20
    ) -> list[dict]:
        """
        Calculates ranked recommendations with guaranteed non-empty category pools.
        Strictly filters candidates by role viability when role is selected.
        Applies smart team composition awareness when role is Any.
        """
        top_k = max(20, top_k)
        heroes_res = await db_session.execute(select(Hero))
        all_heroes = heroes_res.scalars().all()

        # 1. Filter out already picked/banned heroes
        picked_ids = set(ally_ids + enemy_ids)
        candidate_heroes = [h for h in all_heroes if h.id not in picked_ids]

        # 2. STRICT ROLE VIABILITY FILTER
        # When user selects a specific role (e.g. Pos 1 Carry), NEVER show unviable roles (e.g. Pos 5 Crystal Maiden)
        if role is not None:
            candidate_heroes = [
                h for h in candidate_heroes
                if role in HERO_VIABLE_ROLES.get(h.id, [])
            ]

        # 3. Detect Team Composition (Allies)
        filled_roles = set()
        for a_id in ally_ids:
            p_role = HERO_PRIMARY_ROLE.get(a_id)
            if p_role:
                filled_roles.add(p_role)
            else:
                viable = HERO_VIABLE_ROLES.get(a_id, [])
                if viable:
                    filled_roles.add(viable[0])

        has_allied_hard_carry = any(a_id in HARD_CARRIES or HERO_PRIMARY_ROLE.get(a_id) == 1 for a_id in ally_ids)
        missing_roles = [r for r in [1, 2, 3, 4, 5] if r not in filled_roles]

        # 4. Role stats pre-fetch
        role_stats_res = await db_session.execute(select(RoleStat))
        role_stats_list = role_stats_res.scalars().all()

        # Map by (hero_id, role) and (hero_id)
        role_stats_by_hr: dict[tuple[int, int], RoleStat] = {}
        role_stats_best: dict[int, RoleStat] = {}
        for rs in role_stats_list:
            role_stats_by_hr[(rs.hero_id, rs.role)] = rs
            if rs.hero_id not in role_stats_best or rs.winrate > role_stats_best[rs.hero_id].winrate:
                role_stats_best[rs.hero_id] = rs

        # 5. Enemy roles map
        enemy_roles_map = {}
        if enemy_ids:
            for e_id in enemy_ids:
                enemy_roles_map[e_id] = HERO_PRIMARY_ROLE.get(e_id, 3)

        # 6. Matchups pre-fetch
        relevant_ids = enemy_ids + ally_ids
        matchups_map: dict[tuple[int, int], Matchup] = {}
        if relevant_ids:
            matchup_query = select(Matchup).where(
                (Matchup.vs_hero_id.in_(relevant_ids)) | (Matchup.hero_id.in_(relevant_ids))
            )
            matchups_res = await db_session.execute(matchup_query)
            for m in matchups_res.scalars().all():
                matchups_map[(m.hero_id, m.vs_hero_id)] = m

        is_picking_core = (role in CORE_ROLES) if role else False
        role_dominators = set(LANE_DOMINATORS_BY_ROLE.get(role, GLOBAL_LANE_DOMINATORS))

        evaluated_candidates = []

        for hero in candidate_heroes:
            badges = []
            pros = []
            cons = []

            # Determine evaluation role for candidate
            if role is not None:
                eval_role = role
            else:
                viable = HERO_VIABLE_ROLES.get(hero.id, [1, 2, 3, 4, 5])
                matching = [r for r in viable if r in missing_roles]
                if matching:
                    p = HERO_PRIMARY_ROLE.get(hero.id)
                    eval_role = p if p in matching else matching[0]
                else:
                    eval_role = HERO_PRIMARY_ROLE.get(hero.id, viable[0] if viable else 3)

            # ── 1. META SCORE (0 - 100) ──
            rs = role_stats_by_hr.get((hero.id, eval_role)) or role_stats_best.get(hero.id)
            if rs:
                winrate = rs.winrate
                pickrate = rs.pickrate
                tier = rs.tier
                pick_bonus = min(10.0, pickrate * 0.4)
                meta_score = (50.0 + (winrate - 50.0) * 6.0) + pick_bonus
                if tier == "S":
                    meta_score += 5.0
                elif tier == "A":
                    meta_score += 2.5
                elif tier == "C":
                    meta_score -= 3.0
                elif tier == "D":
                    meta_score -= 6.0
            else:
                winrate = 50.0
                pickrate = 2.0
                tier = "B"
                meta_score = 45.0

            meta_score = self.normalize_score(meta_score)

            # ── 2. COUNTER SCORE (Against all picked enemies) ──
            strong_counters = []
            vulnerabilities = []
            max_single_advantage = 0.0
            total_net_counter = 0.0
            has_major_mechanical_counter = False
            top_countered_enemy_id = None
            top_countered_enemy_name = ""
            top_countered_adv = 0.0
            top_mech_reason = ""

            for e_id in enemy_ids:
                enemy_info = HERO_BY_ID.get(e_id, {})
                e_name = enemy_info.get("localized_name_ru", f"Враг #{e_id}")
                e_role = enemy_roles_map.get(e_id, 3)
                is_enemy_support = (e_role in SUPPORT_ROLES)

                # 1. Curated & Mechanical Counter Matrix (50%)
                curated_adv = 0.0
                if (hero.id, e_id) in CURATED_MATCHUPS:
                    curated_adv = CURATED_MATCHUPS[(hero.id, e_id)]
                elif (e_id, hero.id) in CURATED_MATCHUPS:
                    curated_adv = -CURATED_MATCHUPS[(e_id, hero.id)]

                mech_bonus, mech_reasons = get_mechanical_counter_multiplier(hero.id, e_id)
                if mech_bonus > 0:
                    has_major_mechanical_counter = True
                    for mr in mech_reasons:
                        pros.append(f"Механика: {mr} против {e_name}")
                        if not top_mech_reason:
                            top_mech_reason = mr

                curated_mech_score = curated_adv + (mech_bonus * 0.8)

                # 2. Statistical Matchup Score (already smoothed and seeded properly)
                m = matchups_map.get((hero.id, e_id))
                rev_m = matchups_map.get((e_id, hero.id))
                if m:
                    db_stat_adv = m.advantage
                elif rev_m:
                    db_stat_adv = -rev_m.advantage
                else:
                    db_stat_adv = curated_adv

                # 3. Combine statistical matchup score (50%) with curated Hard Counter Matrix & Mechanical Counter Tags (50%)
                if (curated_adv != 0.0 or mech_bonus > 0) and db_stat_adv != 0.0:
                    net_adv = (0.50 * db_stat_adv) + (0.50 * curated_mech_score)
                elif curated_adv != 0.0 or mech_bonus > 0:
                    net_adv = curated_mech_score
                else:
                    net_adv = db_stat_adv

                if net_adv > max_single_advantage:
                    max_single_advantage = net_adv
                    top_countered_enemy_id = e_id
                    top_countered_enemy_name = e_name
                    top_countered_adv = net_adv

                multiplier = 1.25 if (is_picking_core and is_enemy_support) else 1.0
                effective_adv = net_adv * multiplier
                total_net_counter += effective_adv

                if net_adv >= 2.0:
                    strong_counters.append(f"{e_name} (+{net_adv:.1f}%)")
                    pros.append(f"Контрит {e_name} (+{net_adv:.1f}%)")
                elif net_adv <= -2.0:
                    vulnerabilities.append(f"{e_name} ({net_adv:.1f}%)")
                    cons.append(f"Слаб против {e_name} ({net_adv:.1f}%)")

            if enemy_ids:
                counter_score = 50.0 + (total_net_counter * 5.5)
            else:
                lane_dom_bonus = 15.0 if hero.id in role_dominators else 0.0
                counter_score = 50.0 + lane_dom_bonus

            counter_score = self.normalize_score(counter_score)

            # ── 3. SYNERGY SCORE (With all picked allies) ──
            synergy_net = 0.0
            top_synergy_ally_id = None
            top_synergy_ally_name = ""
            top_synergy_val = 0.0

            for a_id in ally_ids:
                ally_info = HERO_BY_ID.get(a_id, {})
                a_name = ally_info.get("localized_name_ru", f"Союзник #{a_id}")
                m = matchups_map.get((hero.id, a_id)) or matchups_map.get((a_id, hero.id))
                syn = m.synergy if m else 0.0
                synergy_net += syn

                if syn > top_synergy_val:
                    top_synergy_val = syn
                    top_synergy_ally_id = a_id
                    top_synergy_ally_name = a_name

                if syn >= 1.5:
                    pros.append(f"Связка с {a_name} (+{syn:.1f}%)")

            if ally_ids:
                synergy_score = 50.0 + (synergy_net * 6.0)
            else:
                synergy_score = 50.0

            synergy_score = self.normalize_score(synergy_score)

            # ── 4. TEAM COMPOSITION ADJUSTMENT (When role is Any) ──
            comp_adjustment = 0.0
            if role is None and ally_ids:
                # Penalize second hard carry if team already has one
                if has_allied_hard_carry and (hero.id in HARD_CARRIES or eval_role == 1):
                    comp_adjustment -= 25.0
                    cons.append("В драфте уже есть керри 1 позиции")
                # Penalize role collision if none of candidate's viable roles are missing
                elif not any(r in missing_roles for r in HERO_VIABLE_ROLES.get(hero.id, [])):
                    comp_adjustment -= 15.0
                    cons.append(f"Позиция {ROLE_NAMES_RU.get(eval_role)} уже закрыта союзниками")
                else:
                    # Rewarded for filling a missing role
                    comp_adjustment += 8.0
                    badges.append(f"🛡️ Баланс драфта: {ROLE_NAMES_RU.get(eval_role)}")
                    pros.append(f"Закрывает дефицит: {ROLE_NAMES_RU.get(eval_role)}")

            # ── 5. TOTAL COMPOSITE SCORE ──
            situational_boost = 0.0
            if enemy_ids:
                if max_single_advantage >= 3.0:
                    situational_boost += 8.0
                if has_major_mechanical_counter:
                    situational_boost += 7.0
                base_score = (0.25 * meta_score) + (0.60 * counter_score) + (0.15 * synergy_score)
                total_score = self.normalize_score(base_score + situational_boost + comp_adjustment)
            else:
                base_score = (0.65 * meta_score) + (0.20 * synergy_score) + (0.15 * counter_score)
                total_score = self.normalize_score(base_score + comp_adjustment)

            if strong_counters:
                badges.append(f"🎯 Жесткий контр: {', '.join(strong_counters[:2])}")
            if hero.id in role_dominators:
                badges.append("⚔️ Доминатор линии")

            unique_badges = list(dict.fromkeys(badges))[:3]

            evaluated_candidates.append({
                "hero": hero,
                "eval_role": eval_role,
                "winrate": winrate,
                "pickrate": pickrate,
                "tier": tier,
                "meta_score": meta_score,
                "counter_score": counter_score,
                "synergy_score": synergy_score,
                "total_score": total_score,
                "max_single_advantage": max_single_advantage,
                "has_major_mechanical_counter": has_major_mechanical_counter,
                "is_lane_dominator": hero.id in role_dominators,
                "top_countered_enemy_id": top_countered_enemy_id,
                "top_countered_enemy_name": top_countered_enemy_name,
                "top_countered_adv": top_countered_adv,
                "top_mech_reason": top_mech_reason,
                "top_synergy_ally_id": top_synergy_ally_id,
                "top_synergy_ally_name": top_synergy_ally_name,
                "top_synergy_val": top_synergy_val,
                "unique_badges": unique_badges,
                "pros": pros,
                "cons": cons
            })

        # ── 6. POOL PARTITIONING (HYBRID, SITUATIONAL, META) ──
        # Pool A (Meta): High patch winrate & synergy
        pool_a = sorted(evaluated_candidates, key=lambda x: (x["meta_score"] * 0.8 + x["synergy_score"] * 0.2), reverse=True)

        # Pool B (Situational): High counter score or lane dominance
        if enemy_ids:
            pool_b = sorted(evaluated_candidates, key=lambda x: (x["counter_score"] * 0.7 + x["max_single_advantage"] * 2.0), reverse=True)
        else:
            pool_b = sorted(evaluated_candidates, key=lambda x: (100.0 if x["is_lane_dominator"] else 0.0) + x["counter_score"], reverse=True)

        # Pool C (Hybrid): High in BOTH
        if enemy_ids:
            pool_c = [
                c for c in evaluated_candidates
                if (c["meta_score"] >= 48.0 and c["counter_score"] >= 52.0) or (c["max_single_advantage"] >= 2.5 and c["winrate"] >= 50.0)
            ]
            pool_c.sort(key=lambda x: x["total_score"], reverse=True)
        else:
            pool_c = [
                c for c in evaluated_candidates
                if c["is_lane_dominator"] and c["winrate"] >= 51.0
            ]
            pool_c.sort(key=lambda x: x["meta_score"], reverse=True)

        # ── 7. SELECTION GUARANTEEING >= 6 SITUATIONAL AND >= 6 META ──
        chosen_map = {} # hero_id -> dict

        # 1. Take top from Hybrid (Pool C)
        for cand in pool_c[:7]:
            cid = cand["hero"].id
            if cid not in chosen_map:
                cand["assigned_category"] = "hybrid"
                cand["assigned_pick_type"] = "meta_counter"
                chosen_map[cid] = cand

        # 2. Take top from Situational (Pool B)
        situational_count = 0
        for cand in pool_b:
            cid = cand["hero"].id
            if cid not in chosen_map:
                cand["assigned_category"] = "situational"
                cand["assigned_pick_type"] = "situational"
                chosen_map[cid] = cand
                situational_count += 1
                if situational_count >= 7:
                    break

        # 3. Take top from Meta (Pool A)
        meta_count = 0
        for cand in pool_a:
            cid = cand["hero"].id
            if cid not in chosen_map:
                cand["assigned_category"] = "meta"
                cand["assigned_pick_type"] = "meta"
                chosen_map[cid] = cand
                meta_count += 1
                if meta_count >= 7:
                    break

        # Fill up to 20-22 if needed
        for cand in pool_a + pool_b:
            if len(chosen_map) >= 22:
                break
            cid = cand["hero"].id
            if cid not in chosen_map:
                cat = "situational" if cand["counter_score"] > cand["meta_score"] else "meta"
                cand["assigned_category"] = cat
                cand["assigned_pick_type"] = cat
                chosen_map[cid] = cand

        final_candidates = list(chosen_map.values())
        final_candidates.sort(key=lambda x: x["total_score"], reverse=True)

        # ── 8. GENERATE DETAILED RUSSIAN REASONS ──
        recommendations = []
        for cand in final_candidates:
            h = cand["hero"]
            cat = cand["assigned_category"]
            pick_type = cand["assigned_pick_type"]
            cand_role = cand["eval_role"]
            role_name = ROLE_NAMES_RU.get(cand_role, "Любая позиция")

            # Rich tactical reason construction using hero-specific ability signatures
            h_sig = HERO_SIGNATURES.get(h.id, {}).get("sig", "реализует свои ключевые способности в драке")
            if enemy_ids and cand["top_countered_enemy_id"] and (cat in ("situational", "hybrid") or cand["max_single_advantage"] >= 1.2):
                reason = generate_tactical_reason(
                    h.id,
                    cand["top_countered_enemy_id"],
                    "counters",
                    cand["top_countered_adv"]
                )
            elif ally_ids and cand["top_synergy_ally_id"] and cand["top_synergy_val"] >= 1.0:
                reason = generate_tactical_reason(
                    h.id,
                    cand["top_synergy_ally_id"],
                    "synergy",
                    cand["top_synergy_val"]
                )
            elif cat == "situational" or cand["is_lane_dominator"]:
                reason = f"{h.localized_name} уверенно доминирует на линии ({role_name}): {h_sig}. Задает высокий темп с первых минут и не дает врагу спокойно фармить."
            elif cat == "hybrid":
                reason = f"{h.localized_name} сочетает высокий винрейт меты ({cand['winrate']:.1f}% WR) и сильный тимфайт: {h_sig}."
            else:
                reason = f"{h.localized_name} — надежный пик текущего патча ({cand['winrate']:.1f}% WR на позиции {role_name}): {h_sig}."

            if len(reason.split()) < 13:
                reason += " Это дает колоссальное позиционное преимущество и гарантирует высокий винрейт."

            recommendations.append({
                "hero_id": h.id,
                "name": h.name,
                "localized_name": h.localized_name,
                "localized_name_ru": h.localized_name_ru,
                "primary_attr": h.primary_attr,
                "attack_type": h.attack_type,
                "icon_url": h.icon_url,
                "score": cand["total_score"],
                "category": cat,         # 'meta' | 'situational' | 'hybrid'
                "pick_type": pick_type,  # 'meta' | 'situational' | 'meta_counter'
                "reason": reason,        # Top-level detailed Russian reason
                "core_items": get_hero_core_items(h.id),
                "situational_items": get_situational_items_for_hero_vs_enemies(h.id, enemy_ids),
                "breakdown": {
                    "total_score": cand["total_score"],
                    "category": cat,
                    "pick_type": pick_type,
                    "meta_score": cand["meta_score"],
                    "counter_score": cand["counter_score"],
                    "synergy_score": cand["synergy_score"],
                    "meta_winrate": cand["winrate"],
                    "meta_pickrate": cand["pickrate"],
                    "tier": cand["tier"],
                    "role": cand_role,
                    "role_name": role_name,
                    "badges": cand["unique_badges"],
                    "pros": cand["pros"][:3],
                    "cons": cand["cons"][:2],
                    "reason": reason
                }
            })

        return recommendations[:top_k]

draft_engine = DraftCalculator()
