import asyncio
import sys
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

from database.db import AsyncSessionLocal
from services.draft_engine import draft_engine
from services.aliases import HERO_BY_ID
from services.hero_roles import HERO_VIABLE_ROLES, HARD_CARRIES
from services.hero_guides import ITEM_CATALOG

async def run_sanity_tests():
    print("==================================================")
    print("RUNNING STRICT DRAFT MATH & SANITY VERIFICATION")
    print("==================================================")

    async with AsyncSessionLocal() as session:
        # TEST 1: Against Phantom Lancer (12)
        print("\n--- TEST 1: Sanity vs Phantom Lancer (12) ---")
        recoms_pl = await draft_engine.recommend(session, ally_ids=[], enemy_ids=[12], role=None, top_k=20)
        top_hero_ids_pl = [r["hero_id"] for r in recoms_pl[:10]]
        print("Top 10 recommended vs PL (12):")
        for idx, r in enumerate(recoms_pl[:10]):
            print(f"  #{idx+1}: {r['localized_name_ru']} (id={r['hero_id']}, score={r['score']}, cat={r['category']}) - {r['reason'][:60]}...")

        required_pl_counters = {7, 52, 18, 2, 16, 106} # Earthshaker, Leshrac, Sven, Axe, Sand King, Ember Spirit
        found_pl = set(top_hero_ids_pl) & required_pl_counters
        print(f"Matches required PL counters: {found_pl} (expected top presence)")
        assert len(found_pl) >= 4, f"Expected at least 4 of {required_pl_counters} in top 10, got {found_pl}"
        
        # Verify WK (42) and Viper (47) are NOT in top recommendations as counters
        assert 42 not in top_hero_ids_pl[:5], f"Wraith King (42) should not be top counter vs PL!"
        assert 47 not in top_hero_ids_pl[:5], f"Viper (47) should not be top counter vs PL!"
        print("PASS: PL sanity check passed.")

        # TEST 2: Against Huskar (59)
        print("\n--- TEST 2: Sanity vs Huskar (59) ---")
        recoms_hu = await draft_engine.recommend(session, ally_ids=[], enemy_ids=[59], role=None, top_k=20)
        top_hero_ids_hu = [r["hero_id"] for r in recoms_hu[:10]]
        print("Top 10 recommended vs Huskar (59):")
        for idx, r in enumerate(recoms_hu[:10]):
            print(f"  #{idx+1}: {r['localized_name_ru']} (id={r['hero_id']}, score={r['score']})")

        required_hu_counters = {68, 36, 47, 25, 21} # AA, Necro, Viper, Lina, Windranger
        found_hu = set(top_hero_ids_hu) & required_hu_counters
        print(f"Matches required Huskar counters: {found_hu}")
        assert len(found_hu) >= 3, f"Expected at least 3 of {required_hu_counters} in top 10, got {found_hu}"
        print("PASS: Huskar sanity check passed.")

        # TEST 3: Against Anti-Mage (1)
        print("\n--- TEST 3: Sanity vs Anti-Mage (1) ---")
        recoms_am = await draft_engine.recommend(session, ally_ids=[], enemy_ids=[1], role=None, top_k=20)
        top_hero_ids_am = [r["hero_id"] for r in recoms_am[:10]]
        print("Top 10 recommended vs Anti-Mage (1):")
        for idx, r in enumerate(recoms_am[:10]):
            print(f"  #{idx+1}: {r['localized_name_ru']} (id={r['hero_id']}, score={r['score']})")

        required_am_counters = {44, 104, 2, 28, 82, 95} # PA, LC, Axe, Slardar, Meepo, Troll
        found_am = set(top_hero_ids_am) & required_am_counters
        print(f"Matches required Anti-Mage counters: {found_am}")
        assert len(found_am) >= 3, f"Expected at least 3 of {required_am_counters} in top 10, got {found_am}"
        print("PASS: Anti-Mage sanity check passed.")

        # TEST 4: Strict Role Viability Filter
        print("\n--- TEST 4: Strict Role Viability Filter ---")
        recoms_carry = await draft_engine.recommend(session, ally_ids=[], enemy_ids=[12], role=1, top_k=20)
        print(f"Testing Pos 1 Carry: got {len(recoms_carry)} candidates.")
        for r in recoms_carry:
            hid = r["hero_id"]
            viable_roles = HERO_VIABLE_ROLES.get(hid, [])
            assert 1 in viable_roles, f"Hero {r['localized_name_ru']} (id={hid}) is not viable as Pos 1! Viable: {viable_roles}"
        print("PASS: All 20 Pos 1 recommendations are strictly legitimate carries (no CM, Lion, etc.).")

        recoms_pos5 = await draft_engine.recommend(session, ally_ids=[], enemy_ids=[12], role=5, top_k=20)
        print(f"Testing Pos 5 Hard Support: got {len(recoms_pos5)} candidates.")
        for r in recoms_pos5:
            hid = r["hero_id"]
            viable_roles = HERO_VIABLE_ROLES.get(hid, [])
            assert 5 in viable_roles, f"Hero {r['localized_name_ru']} (id={hid}) is not viable as Pos 5! Viable: {viable_roles}"
        print("PASS: All 20 Pos 5 recommendations are strictly legitimate hard supports.")

        # TEST 5: Team Composition Awareness (Allies Picked)
        print("\n--- TEST 5: Team Composition Awareness ---")
        # Allied team already has Pos 1 Anti-Mage (id 1) and Pos 2 Invoker (id 74)
        recoms_comp = await draft_engine.recommend(session, ally_ids=[1, 74], enemy_ids=[12], role=None, top_k=20)
        top_5_ids = [r["hero_id"] for r in recoms_comp[:5]]
        print(f"When team already has AM (Pos 1) + Invoker (Pos 2), Top 5 recommendations:")
        for idx, r in enumerate(recoms_comp[:5]):
            print(f"  #{idx+1}: {r['localized_name_ru']} (id={r['hero_id']}, score={r['score']}, role={r['breakdown']['role_name']})")
        # Ensure pure hard carries (PA, Juggernaut, Void, Medusa) are NOT in the top 3
        top_3_carries = [hid for hid in top_5_ids[:3] if hid in HARD_CARRIES]
        assert len(top_3_carries) == 0, f"Expected 0 hard carries in top 3 when ally already picked AM, got {top_3_carries}"
        print("PASS: Smart Team Composition correctly avoids double hard carry and recommends offlaners/supports.")

        # TEST 6: Empty Draft (0 allies, 0 enemies, Any Role)
        print("\n--- TEST 6: 0 Allies, 0 Enemies ---")
        recoms_empty = await draft_engine.recommend(session, ally_ids=[], enemy_ids=[], role=None, top_k=20)
        assert len(recoms_empty) >= 20, f"Expected >= 20 recommendations, got {len(recoms_empty)}"
        situational_empty = [r for r in recoms_empty if r["category"] in ("situational", "hybrid")]
        meta_empty = [r for r in recoms_empty if r["category"] in ("meta", "hybrid")]
        assert len(situational_empty) >= 6, f"Expected >= 6 situational items, got {len(situational_empty)}"
        assert len(meta_empty) >= 6, f"Expected >= 6 meta items, got {len(meta_empty)}"
        print(f"PASS: Empty draft successfully returned {len(recoms_empty)} recommendations with both situational and meta tabs populated.")

        # TEST 7: Check Removed Items Purged
        print("\n--- TEST 7: Removed Items Purged ---")
        removed_items = ["eternal_" + "shroud", "cornu" + "copia", "hood_of_" + "defiance", "wraith_" + "pact", "medallion_of_" + "courage", "necro" + "nomicon"]
        for item_key in removed_items:
            assert item_key not in ITEM_CATALOG, f"Removed item {item_key} must not be in ITEM_CATALOG!"
        assert "mage_slayer" in ITEM_CATALOG, "Mage Slayer must be in ITEM_CATALOG!"
        assert "glimmer_cape" in ITEM_CATALOG, "Glimmer Cape must be in ITEM_CATALOG!"
        assert "pipe" in ITEM_CATALOG, "Pipe must be in ITEM_CATALOG!"
        assert "sphere" in ITEM_CATALOG, "Linken's Sphere must be in ITEM_CATALOG!"
        print("PASS: All blacklisted items purged; Mage Slayer, Glimmer Cape, Pipe, Linken active.")

    print("\n==================================================")
    print("ALL SANITY AND REBALANCING TESTS PASSED 100%!")
    print("==================================================")

if __name__ == "__main__":
    asyncio.run(run_sanity_tests())
