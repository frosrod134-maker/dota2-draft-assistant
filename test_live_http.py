import urllib.request
import json

tunnel = "https://8f322565648270.lhr.life"

print("--- Testing Live Empty Draft (allies: [], enemies: [], role: 'any') ---")
req1 = urllib.request.Request(
    f"{tunnel}/api/recommend",
    data=json.dumps({"allies": [], "enemies": [], "role": "any"}).encode("utf-8"),
    headers={"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}
)
res1 = json.loads(urllib.request.urlopen(req1).read().decode())
recoms1 = res1.get("recommendations", [])
print(f"Empty draft recommendations returned: {len(recoms1)}")
assert len(recoms1) >= 20, f"Expected >= 20, got {len(recoms1)}"
print("PASS: Empty draft returned 20 valid recommendations without error.")

print("\n--- Testing Live vs PL, ally Lion, role 1 (Carry) ---")
req2 = urllib.request.Request(
    f"{tunnel}/api/recommend",
    data=json.dumps({"enemies": ["Phantom Lancer"], "allies": ["Lion"], "role": 1}).encode("utf-8"),
    headers={"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}
)
res2 = json.loads(urllib.request.urlopen(req2).read().decode())
recoms2 = res2.get("recommendations", [])
print(f"Recommendations returned: {len(recoms2)}")
top_carries = [r["localized_name"] for r in recoms2[:7]]
print(f"Top Pos 1 carries vs PL: {top_carries}")
expected = {"Sven", "Leshrac", "Gyrocopter", "Luna", "Naga Siren", "Muerta"}
found_expected = [c for c in top_carries if c in expected]
print(f"Canonical carry counters present: {found_expected}")
assert len(found_expected) >= 4, f"Expected at least 4 of {expected}, got {found_expected}"
print("PASS: Canonical Pos 1 carries that counter PL dominate the top recommendations!")

print("\n==============================================")
print("ALL LIVE HTTP VERIFICATIONS PASSED 100%!")
print("==============================================")
