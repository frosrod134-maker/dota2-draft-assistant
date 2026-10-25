import logging
import httpx
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from database.models import Hero, RoleStat, Matchup
from services.aliases import HERO_LIST, HERO_BY_ID
from config import settings

logger = logging.getLogger("seed_data")

# Baseline meta role mappings for major heroes (Roles: 1=Carry, 2=Mid, 3=Offlane, 4=Soft Supp, 5=Hard Supp)
BASELINE_ROLE_STATS = {
    # Carries (Pos 1)
    1: [(1, 52.4, 18.5, "S")],    # Anti-Mage
    8: [(1, 51.8, 22.0, "S")],    # Juggernaut
    10: [(1, 53.2, 12.0, "S")],   # Morphling
    12: [(1, 50.5, 9.5, "A")],    # Phantom Lancer
    18: [(1, 51.2, 14.0, "A")],   # Sven
    41: [(1, 52.8, 16.0, "S")],   # Faceless Void
    42: [(1, 51.0, 11.0, "B")],   # Wraith King
    44: [(1, 53.5, 24.0, "S")],   # Phantom Assassin
    48: [(1, 52.1, 15.0, "A")],   # Luna
    54: [(1, 52.9, 19.0, "S")],   # Lifestealer
    63: [(1, 51.4, 13.0, "A")],   # Weaver
    70: [(1, 53.0, 14.5, "S")],   # Ursa
    81: [(1, 52.3, 10.0, "A")],   # Chaos Knight
    93: [(1, 52.6, 17.0, "S")],   # Slark
    94: [(1, 51.9, 12.0, "A")],   # Medusa
    95: [(1, 51.1, 8.5, "B")],    # Troll Warlord
    109: [(1, 50.8, 9.0, "B")],   # Terrorblade
    114: [(1, 51.5, 13.5, "A")],  # Monkey King
    145: [(1, 53.8, 15.0, "S")],  # Kez

    # Midlaners (Pos 2)
    11: [(2, 52.6, 20.0, "S")],   # Shadow Fiend
    13: [(2, 53.1, 14.0, "S")],   # Puck
    17: [(2, 52.2, 16.0, "A")],   # Storm Spirit
    22: [(2, 51.9, 15.0, "A")],   # Zeus
    25: [(2, 53.4, 18.0, "S")],   # Lina
    34: [(2, 51.5, 11.0, "B")],   # Tinker
    35: [(2, 52.0, 25.0, "S"), (1, 50.8, 8.0, "B")], # Sniper
    39: [(2, 52.7, 17.0, "S")],   # Queen of Pain
    46: [(2, 53.0, 14.0, "S")],   # Templar Assassin
    74: [(2, 52.5, 22.0, "S")],   # Invoker
    76: [(2, 51.8, 12.0, "A")],   # Outworld Destroyer
    106: [(2, 52.9, 15.5, "S")],  # Ember Spirit
    120: [(2, 52.1, 10.0, "A")],  # Pangolier
    126: [(2, 51.7, 11.5, "A")],  # Void Spirit

    # Offlaners (Pos 3)
    2: [(3, 52.8, 21.0, "S")],    # Axe
    14: [(3, 50.9, 15.0, "A"), (4, 51.4, 25.0, "S")], # Pudge
    16: [(3, 52.3, 13.0, "A")],   # Sand King
    28: [(3, 53.2, 16.0, "S")],   # Slardar
    29: [(3, 51.5, 14.0, "A")],   # Tidehunter
    38: [(3, 52.0, 9.0, "A")],    # Beastmaster
    49: [(3, 52.5, 17.0, "S"), (2, 51.2, 8.0, "B")], # Dragon Knight
    55: [(3, 53.6, 8.0, "S")],    # Dark Seer
    96: [(3, 52.7, 19.0, "S")],   # Centaur Warrunner
    97: [(3, 51.4, 12.0, "A")],   # Magnus
    98: [(3, 52.2, 11.0, "A")],   # Timbersaw
    99: [(3, 52.9, 16.5, "S")],   # Bristleback
    104: [(3, 51.8, 18.0, "A")],  # Legion Commander
    108: [(3, 53.0, 10.0, "S")],  # Underlord
    129: [(3, 52.4, 17.5, "S")],  # Mars
    135: [(3, 52.1, 12.0, "A")],  # Dawnbreaker
    137: [(3, 53.3, 14.0, "S")],  # Primal Beast

    # Soft Supports (Pos 4)
    4: [(4, 50.2, 8.0, "B")],
    7: [(4, 52.6, 18.0, "S")],    # Earthshaker
    9: [(4, 51.5, 14.0, "A")],    # Mirana
    20: [(4, 52.0, 12.0, "A")],   # Vengeful Spirit
    21: [(4, 51.8, 11.0, "A")],   # Windranger
    26: [(4, 52.2, 23.0, "S"), (5, 51.0, 15.0, "A")], # Lion
    51: [(4, 52.7, 10.5, "S")],   # Clockwerk
    62: [(4, 51.3, 13.0, "A")],   # Bounty Hunter
    86: [(4, 52.5, 26.0, "S")],   # Rubick
    88: [(4, 52.8, 12.0, "S")],   # Nyx Assassin
    100: [(4, 51.9, 11.0, "A")],  # Tusk
    107: [(4, 52.1, 9.0, "A")],   # Earth Spirit
    119: [(4, 51.4, 8.5, "B")],   # Dark Willow
    121: [(4, 51.6, 10.0, "A")],  # Grimstroke
    123: [(4, 52.3, 16.0, "S")],  # Hoodwink
    136: [(4, 52.0, 9.5, "A")],   # Marci

    # Hard Supports (Pos 5)
    3: [(5, 51.4, 9.0, "A")],     # Bane
    5: [(5, 52.7, 21.0, "S")],    # Crystal Maiden
    27: [(5, 52.2, 17.0, "S")],   # Shadow Shaman
    30: [(5, 53.4, 25.0, "S")],   # Witch Doctor
    31: [(5, 52.8, 16.0, "S")],   # Lich
    37: [(5, 53.1, 14.0, "S")],   # Warlock
    50: [(5, 52.0, 15.0, "A")],   # Dazzle
    57: [(5, 51.2, 9.0, "B")],    # Omniknight
    58: [(5, 51.5, 7.5, "B")],    # Enchantress
    64: [(5, 52.9, 19.0, "S")],   # Jakiro
    66: [(5, 54.1, 4.0, "S")],    # Chen
    68: [(5, 52.3, 13.0, "A")],   # Ancient Apparition
    83: [(5, 53.0, 11.0, "S")],   # Treant Protector
    84: [(5, 52.1, 18.0, "A")],   # Ogre Magi
    85: [(5, 52.6, 14.5, "S")],   # Undying
    87: [(5, 52.4, 15.0, "A")],   # Disruptor
    90: [(5, 51.8, 12.0, "A")],   # Keeper of the Light
    91: [(5, 51.0, 5.0, "B")],    # Io
    111: [(5, 52.2, 8.0, "A")],   # Oracle
    112: [(5, 52.5, 11.0, "A")],  # Winter Wyvern
    128: [(5, 52.0, 13.0, "A")],  # Snapfire
    139: [(5, 51.9, 14.0, "A")],  # Ringmaster
}

# Strong counters baseline table: (Hero A, Hero B, Advantage, Synergy)
# Advantage > 0: Hero A counters Hero B (positive advantage for Hero A)
BASELINE_MATCHUPS = [
    # ── Against Phantom Lancer (12) ──
    (7, 12, 8.5, 2.0),    # Earthshaker counters PL (Echo Slam destroys illusions)
    (52, 12, 7.8, 1.5),   # Leshrac counters PL (Pulse Nova clears all copies)
    (18, 12, 7.5, 1.8),   # Sven counters PL (Great Cleave 2-shots army)
    (72, 12, 7.2, 1.6),   # Gyrocopter counters PL (Flak Cannon destroys illusions across teamfights)
    (2, 12, 7.2, 1.8),    # Axe counters PL (Call + Helix helixes copies)
    (48, 12, 7.0, 1.5),   # Luna counters PL (Moon Glaives ricochet cuts down illusions in seconds)
    (89, 12, 6.8, 1.4),   # Naga Siren counters PL (Stronger illusions, Rip Tide AoE damage and armor reduction)
    (16, 12, 6.8, 1.6),   # Sand King counters PL (Epicenter / Sand Storm)
    (138, 12, 6.6, 1.2),  # Muerta counters PL (Pierce the Veil magical burst, Dead Shot & Calling AoE)
    (106, 12, 6.5, 1.4),  # Ember Spirit counters PL (Sleight of Fist)
    (98, 12, 6.2, 1.2),   # Timbersaw counters PL (Reactive Armor + Pure Chakram)
    (99, 12, 5.8, 1.0),   # Bristleback counters PL (Quill Spray stacks)
    (12, 42, 6.5, 1.2),   # PL counters Wraith King (Mana burn drains Reincarnation)
    (12, 47, 5.8, 1.0),   # PL counters Viper (Single-target can't deal with copies)
    (12, 94, 7.0, 1.5),   # PL counters Medusa (Diffusal strips Mana Shield instantly)
    (12, 1, 5.5, 1.2),    # PL counters Anti-Mage (Mass mana burn)
    (12, 6, 6.0, 1.0),    # PL counters Drow Ranger (Phantom Rush jumps in)
    (12, 35, 5.8, 1.0),   # PL counters Sniper (Swarmed by illusions)

    # ── Against Huskar (59) ──
    (68, 59, 9.0, 1.2),   # Ancient Apparition counters Huskar (Ice Blast stops all heal)
    (36, 59, 7.8, 1.5),   # Necrophos counters Huskar (Reaper's Scythe % HP execute)
    (47, 59, 7.2, 1.2),   # Viper counters Huskar (Nethertoxin Break + Corrosive)
    (25, 59, 6.8, 1.0),   # Lina counters Huskar (Laguna Blade pure burst)
    (21, 59, 6.2, 1.4),   # Windranger counters Huskar (Windrun + Focus Fire shackle)
    (33, 59, 5.8, 1.8),   # Enigma counters Huskar (Midnight Pulse % HP burn)
    (98, 59, 5.5, 1.1),   # Timbersaw counters Huskar (Pure damage ignores magic resist)
    (59, 46, 6.5, 1.2),   # Huskar counters Templar Assassin (Burning spears burn refraction)
    (59, 49, 5.8, 1.0),   # Huskar counters Dragon Knight (Magic spears destroy armor)
    (59, 22, 6.2, 1.0),   # Huskar counters Zeus (Berserker Blood 80% magic resistance)
    (59, 23, 5.5, 1.2),   # Huskar counters Kunkka (Survives combo and out-sustains)

    # ── Against Anti-Mage (1) ──
    (44, 1, 7.8, 1.2),    # Phantom Assassin counters AM (Coup de Grace physical 1-shot)
    (104, 1, 7.5, 1.5),   # Legion Commander counters AM (Duel through Counterspell)
    (2, 1, 7.2, 1.5),     # Axe counters AM (Berserker Call through Counterspell)
    (28, 1, 6.8, 1.4),    # Slardar counters AM (Corrosive Haze + Bash through BKB)
    (82, 1, 6.5, 1.0),    # Meepo counters AM (Earthbind chain root stops Blink)
    (95, 1, 6.2, 1.1),    # Troll Warlord counters AM (Whirling Axes root/bash)
    (93, 1, 5.8, 1.2),    # Slark counters AM (Pounce leash + Essence Shift)
    (4, 1, 5.5, 1.2),     # Bloodseeker counters AM (Rupture stops Blink)
    (71, 1, 5.2, 1.8),    # Spirit Breaker counters AM (Charge vision + BKB bash)
    (1, 94, 7.5, 1.2),    # AM counters Medusa (Mana Void explodes huge mana pool)
    (1, 17, 6.8, 1.0),    # AM counters Storm Spirit (Mana burn prevents Ball Lightning)
    (1, 22, 7.0, 0.5),    # AM counters Zeus (Magic resistance + Mana Void)
    (1, 52, 6.5, 1.2),    # AM counters Leshrac (Mana burn explodes Leshrac)
    (1, 76, 6.0, 1.0),    # AM counters Outworld Destroyer (Mana Void on high INT)
    (1, 34, 5.5, 1.0),    # AM counters Tinker (Blinks on top of trees)
    (1, 74, 5.0, 1.2),    # AM counters Invoker (Resists spells, burns mana)

    # ── Against Meepo (82) ──
    (112, 82, 8.5, 1.5),  # Winter Wyvern counters Meepo (Curse kills clone)
    (7, 82, 8.0, 1.8),    # Earthshaker counters Meepo (Echo Slam multikill)
    (103, 82, 7.5, 1.4),  # Elder Titan counters Meepo (Astral Spirit + stomp)
    (18, 82, 6.8, 1.5),   # Sven counters Meepo (Cleave kills all clones)
    (52, 82, 6.5, 1.2),   # Leshrac counters Meepo (Pulse Nova AoE)

    # ── Against Morphling (10) ──
    (68, 10, 8.5, 1.2),   # AA counters Morphling (Ice Blast stops attribute shift)
    (76, 10, 6.8, 1.0),   # OD counters Morphling (Sanity Eclipse pure INT blast)
    (26, 10, 6.0, 1.5),   # Lion counters Morphling (Instant Mana Drain + Finger)
    (4, 10, 5.8, 1.2),    # Bloodseeker counters Morphling (Rupture vs waveform)

    # ── Against Bristleback (99) ──
    (47, 99, 8.0, 1.2),   # Viper counters Bristleback (Nethertoxin Break)
    (98, 99, 7.5, 1.2),   # Timbersaw counters Bristleback (Pure damage + str steal)
    (104, 99, 6.5, 1.4),  # Legion Commander counters Bristleback (Duel locks back)
    (36, 99, 6.2, 1.6),   # Necrophos counters Bristleback (Heartstopper + execute)

    # ── Against Slark (93) ──
    (4, 93, 8.0, 1.4),    # Bloodseeker counters Slark (Thirst detects invis)
    (87, 93, 7.0, 1.8),   # Disruptor counters Slark (Static Storm + Kinetic)
    (52, 93, 6.5, 1.2),   # Leshrac counters Slark (AoE hits through Shadow Dance)
    (2, 93, 6.0, 1.5),    # Axe counters Slark (Call locks Slark)

    # ── Against Drow Ranger (6) & Sniper (35) ──
    (71, 6, 7.5, 1.8),    # Spirit Breaker counters Drow
    (51, 6, 7.2, 1.5),    # Clockwerk counters Drow
    (67, 6, 7.0, 1.2),    # Spectre counters Drow
    (17, 6, 6.8, 1.2),    # Storm Spirit counters Drow
    (44, 6, 6.5, 1.0),    # PA counters Drow
    (71, 35, 7.8, 1.8),   # Spirit Breaker counters Sniper
    (51, 35, 7.5, 1.5),   # Clockwerk counters Sniper
    (67, 35, 7.2, 1.2),   # Spectre counters Sniper
    (14, 35, 6.5, 1.5),   # Pudge counters Sniper
    (17, 35, 7.0, 1.0),   # Storm counters Sniper

    # ── Big Teamfight Counters ──
    (75, 33, 8.5, 2.5),   # Silencer counters Enigma (Global vs Black Hole)
    (86, 33, 7.0, 2.0),   # Rubick counters Enigma (Steals Black Hole)
    (75, 29, 6.2, 2.0),   # Silencer vs Tidehunter
    (75, 97, 5.8, 2.2),   # Silencer vs Magnus
    (75, 13, 5.4, 1.5),   # Silencer vs Puck

    # ── Pudge Counters & Targets ──
    (14, 26, 4.0, 2.0),   # Pudge vs Lion
    (14, 5, 4.5, 1.7),    # Pudge vs Crystal Maiden
    (54, 14, 7.5, 1.5),   # Lifestealer counters Pudge (% HP feast)
    (70, 14, 7.0, 1.2),   # Ursa counters Pudge (Fury Swipes shreds HP)
    (98, 14, 6.5, 1.4),   # Timbersaw counters Pudge (Pure damage)

    # ── Top Synergy Combos ──
    (41, 74, 4.2, 4.0),   # Void + Invoker (Chrono + Cataclysm)
    (41, 30, 3.9, 3.8),   # Void + Witch Doctor (Chrono + Death Ward)
    (41, 22, 3.5, 3.5),   # Void + Zeus (Chrono + Nimbus)
    (97, 18, 4.0, 4.5),   # Magnus + Sven (RP + Empower + Cleave)
    (97, 44, 3.8, 4.0),   # Magnus + PA (RP + Empower)
    (97, 8, 3.6, 3.8),    # Magnus + Juggernaut
    (84, 12, 3.5, 4.2),   # Ogre + PL (Bloodlust)
    (50, 59, 3.5, 4.5),   # Dazzle + Huskar (Grave + Heal)
    (87, 89, 3.8, 4.0),   # Disruptor + Naga (Song + Static Storm setup)
]

async def seed_database(session: AsyncSession, force: bool = False):
    """
    Seeds heroes, role stats, and matchup counters into the database.
    Ensures the DB is never empty on first launch.
    """
    # 1. Check if heroes already exist
    result = await session.execute(select(func.count(Hero.id)))
    hero_count = result.scalar()

    if hero_count == 0 or force:
        logger.info("[Seed] Seeding Dota 2 heroes from aliases...")
        for h_data in HERO_LIST:
            existing = await session.get(Hero, h_data["id"])
            if not existing:
                hero = Hero(
                    id=h_data["id"],
                    name=h_data["name"],
                    localized_name=h_data["localized_name"],
                    localized_name_ru=h_data["localized_name_ru"],
                    primary_attr=h_data["primary_attr"],
                    attack_type=h_data["attack_type"],
                    roles=h_data["roles"],
                    icon_url=h_data["icon_url"],
                    aliases=",".join(h_data["aliases"])
                )
                session.add(hero)
            else:
                existing.localized_name = h_data["localized_name"]
                existing.localized_name_ru = h_data["localized_name_ru"]
                existing.aliases = ",".join(h_data["aliases"])
        await session.commit()
        logger.info(f"[Seed] Successfully seeded {len(HERO_LIST)} heroes.")
    else:
        # Keep existing SQLite database updated with fresh Russian names and aliases
        for h_data in HERO_LIST:
            existing = await session.get(Hero, h_data["id"])
            if existing:
                existing.localized_name = h_data["localized_name"]
                existing.localized_name_ru = h_data["localized_name_ru"]
                existing.aliases = ",".join(h_data["aliases"])
        await session.commit()
        logger.info(f"[Seed] Updated localized names and aliases for {len(HERO_LIST)} heroes.")

    # 2. Check and seed RoleStats
    role_count_res = await session.execute(select(func.count(RoleStat.id)))
    role_count = role_count_res.scalar()

    if role_count == 0 or force:
        logger.info("[Seed] Seeding baseline D2PT Role Stats...")
        seeded_heroes = set()
        # Populate explicit meta stats
        for hero_id, stats in BASELINE_ROLE_STATS.items():
            for role_num, wr, pr, tier in stats:
                rs = RoleStat(
                    hero_id=hero_id,
                    role=role_num,
                    matches=int(pr * 150),
                    winrate=wr,
                    pickrate=pr,
                    tier=tier
                )
                session.add(rs)
                seeded_heroes.add(hero_id)

        # For any hero without explicit role stats, add a reasonable default based on primary attr
        for h_data in HERO_LIST:
            hid = h_data["id"]
            if hid not in seeded_heroes:
                if h_data["primary_attr"] == "agi":
                    default_role = 1
                elif h_data["primary_attr"] == "str":
                    default_role = 3
                else:
                    default_role = 5
                session.add(RoleStat(
                    hero_id=hid,
                    role=default_role,
                    matches=1000,
                    winrate=50.0,
                    pickrate=5.0,
                    tier="B"
                ))
        await session.commit()
        logger.info("[Seed] Role stats seeded successfully.")

    # 3. Check and seed Matchups
    matchup_count_res = await session.execute(select(func.count(Matchup.id)))
    matchup_count = matchup_count_res.scalar()

    if matchup_count == 0 or force:
        logger.info("[Seed] Seeding baseline Hero Counter Matchups...")
        for hero_a, hero_b, adv, syn in BASELINE_MATCHUPS:
            # A vs B
            session.add(Matchup(
                hero_id=hero_a,
                vs_hero_id=hero_b,
                advantage=adv,
                winrate=50.0 + (adv * 1.5),
                games_played=80,
                synergy=syn
            ))
            # Reverse: B vs A has negative advantage
            session.add(Matchup(
                hero_id=hero_b,
                vs_hero_id=hero_a,
                advantage=-adv,
                winrate=50.0 - (adv * 1.5),
                games_played=80,
                synergy=syn
            ))
        await session.commit()
        logger.info("[Seed] Matchups seeded successfully.")

    # 4. Optional: Try to fetch fresh OpenDota winrates in the background
    try:
        await fetch_opendota_hero_stats(session)
    except Exception as e:
        logger.warning(f"[Seed] OpenDota online sync skipped or failed (using baseline): {e}")

async def fetch_opendota_hero_stats(session: AsyncSession):
    """
    Fetches real-time hero statistics from OpenDota API to refine winrates.
    """
    async with httpx.AsyncClient(timeout=6.0) as client:
        resp = await client.get(f"{settings.OPENDOTA_API_URL}/heroStats")
        if resp.status_code == 200:
            data = resp.json()
            for item in data:
                hero_id = item.get("id")
                # Calculate high-tier winrate (Divine / Immortal matches: 8_win / 8_pick)
                pro_pick = item.get("8_pick", 0) + item.get("7_pick", 0)
                pro_win = item.get("8_win", 0) + item.get("7_win", 0)
                if pro_pick > 100:
                    wr = (pro_win / pro_pick) * 100.0
                    # Update all role stats for this hero with real winrate baseline
                    q = select(RoleStat).where(RoleStat.hero_id == hero_id)
                    res = await session.execute(q)
                    for r_stat in res.scalars().all():
                        # Blend 70% online WR + 30% role-specific adjustment
                        r_stat.winrate = round((wr * 0.7) + (r_stat.winrate * 0.3), 2)
            await session.commit()
            logger.info("[Seed] Successfully enriched hero winrates from OpenDota API.")
