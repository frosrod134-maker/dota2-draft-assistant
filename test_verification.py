import sys
import json
import httpx

BASE_URL = "http://127.0.0.1:8000"

def log(msg):
    sys.stdout.buffer.write((msg + "\n").encode("utf-8"))
    sys.stdout.buffer.flush()

def test_all():
    client = httpx.Client(base_url=BASE_URL, timeout=10.0)

    # 1. PATCH TEST
    log("=== 1. TESTING /api/patch ===")
    r = client.get("/api/patch")
    assert r.status_code == 200, f"Patch endpoint failed: {r.status_code}"
    patch_data = r.json()
    log(f"Patch data: {json.dumps(patch_data, ensure_ascii=False)}")
    assert "7.41f" in patch_data.get("patch", "") or "7.41f" in patch_data.get("raw_patch", ""), "Patch must be 7.41f"
    log("PASS: Patch 7.41f verified.")

    # 2. RECOMMENDATIONS TESTS
    log("\n=== 2. TESTING /api/recommend ===")
    test_cases = [
        ("0 enemies", {"ally_ids": [], "enemy_ids": [], "role": None, "top_k": 20}),
        ("2 supports", {"ally_ids": [], "enemy_ids": [26, 30], "role": 1, "top_k": 20}),
        ("5 enemies", {"ally_ids": [1], "enemy_ids": [12, 26, 30, 2, 74], "role": 2, "top_k": 20})
    ]

    for label, payload in test_cases:
        log(f"\n--- Testing Draft Recommend with: {label} ---")
        res = client.post("/api/recommend", json=payload)
        assert res.status_code == 200, f"Recommend error {res.status_code}: {res.text}"
        data = res.json()
        recoms = data.get("recommendations", [])
        log(f"Returned {len(recoms)} recommendations.")
        assert len(recoms) >= 18, f"Expected at least 18 recommendations, got {len(recoms)}"

        situational_count = sum(1 for r in recoms if r.get("category") in ("situational", "hybrid"))
        meta_count = sum(1 for r in recoms if r.get("category") in ("meta", "hybrid"))

        log(f"Category counts: Situational/Hybrid={situational_count}, Meta/Hybrid={meta_count}")
        assert situational_count >= 6, f"Expected >= 6 situational items, got {situational_count}"
        assert meta_count >= 6, f"Expected >= 6 meta items, got {meta_count}"

        for idx, r in enumerate(recoms[:5]):
            reason = r.get("reason", "")
            words = reason.split()
            log(f"  #{idx+1} {r.get('localized_name_ru')} [{r.get('category')}]: {reason}")
            assert len(words) >= 8, f"Reason too short for #{idx+1} {r.get('localized_name_ru')}: {reason}"
        log(f"PASS: Recommend check for '{label}' passed successfully.")

    # 3. HERO GUIDES TESTS (10 Heroes)
    log("\n=== 3. TESTING /api/heroes/{id}/guide (10 Heroes) ===")
    hero_ids_to_test = [1, 12, 26, 70, 74, 82, 89, 93, 94, 137]

    for hid in hero_ids_to_test:
        r = client.get(f"/api/heroes/{hid}/guide")
        assert r.status_code == 200, f"Guide for hero {hid} failed: {r.status_code}"
        guide = r.json().get("guide", {})
        hero_info = guide.get("hero", {})
        hname = hero_info.get("name_ru", f"Hero {hid}")

        hard_counters = guide.get("hard_counters", [])
        strong_against = guide.get("strong_against", [])
        synergies = guide.get("best_synergies", [])
        counter_items = guide.get("counter_items", [])
        tactics = guide.get("tactics", {})

        hc_ids = {c["hero_id"] for c in hard_counters}
        sa_ids = {s["hero_id"] for s in strong_against}
        syn_ids = {syn["hero_id"] for syn in synergies}

        # Check counts
        assert len(hard_counters) == 6, f"Hero {hname}: expected 6 hard counters, got {len(hard_counters)}"
        assert len(strong_against) == 6, f"Hero {hname}: expected 6 strong against, got {len(strong_against)}"
        assert len(synergies) >= 5, f"Hero {hname}: expected >= 5 synergies, got {len(synergies)}"
        assert len(counter_items) >= 4, f"Hero {hname}: expected >= 4 counter items, got {len(counter_items)}"

        # Check ZERO overlap
        overlap_hc_sa = hc_ids & sa_ids
        overlap_hc_syn = hc_ids & syn_ids
        overlap_sa_syn = sa_ids & syn_ids
        assert not overlap_hc_sa, f"Hero {hname}: Overlap between Hard Counters and Strong Against: {overlap_hc_sa}"
        assert not overlap_hc_syn, f"Hero {hname}: Overlap between Hard Counters and Synergies: {overlap_hc_syn}"
        assert not overlap_sa_syn, f"Hero {hname}: Overlap between Strong Against and Synergies: {overlap_sa_syn}"
        assert hid not in (hc_ids | sa_ids | syn_ids), f"Hero {hname} appears in their own matchup list!"

        # Check icons and reasons for hard counters
        for c in hard_counters:
            assert c["icon_url"].startswith("https://"), f"Invalid icon for {c['name_ru']}"
            assert len(c["reason"].split()) >= 6, f"Reason too short in hard_counters for {hname} vs {c['name_ru']}: {c['reason']}"

        # Check icons and reasons for strong against
        for s in strong_against:
            assert s["icon_url"].startswith("https://"), f"Invalid icon for {s['name_ru']}"
            assert len(s["reason"].split()) >= 6, f"Reason too short in strong_against for {hname} vs {s['name_ru']}: {s['reason']}"

        # Check icons and reasons for synergies
        for syn in synergies:
            assert syn["icon_url"].startswith("https://"), f"Invalid icon for {syn['name_ru']}"
            assert len(syn["reason"].split()) >= 6, f"Reason too short in synergies for {hname} with {syn['name_ru']}: {syn['reason']}"

        # Check items
        for item in counter_items:
            assert item["icon_url"].startswith("https://"), f"Invalid item icon for {item['name_ru']}"
            assert len(item["reason"].split()) >= 5, f"Item reason too short for {hname} - {item['name_ru']}: {item['reason']}"

        # Check tactics
        assert len(tactics.get("strengths", "")) > 10
        assert len(tactics.get("weaknesses", "")) > 10
        assert len(tactics.get("how_to_play_against", "")) > 10

        log(f"PASS: Hero {hname} (ID {hid}) guide verified! (0 overlaps, full Russian reasons, CDN icons)")

    log("\n==========================================")
    log("ALL VERIFICATION CHECKS PASSED PERFECTLY!")
    log("==========================================")

if __name__ == "__main__":
    test_all()
