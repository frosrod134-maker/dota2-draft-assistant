import asyncio
import sys
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")
from database.db import AsyncSessionLocal
from database.models import Matchup, RoleStat, Hero
from sqlalchemy import select
from services.aliases import HERO_BY_ID

async def check():
    async with AsyncSessionLocal() as s:
        # Check against PL (12)
        r = await s.execute(select(Matchup).where(Matchup.vs_hero_id == 12).order_by(Matchup.advantage.desc()).limit(10))
        print("Top vs PL (12):")
        for m in r.scalars():
            name = HERO_BY_ID.get(m.hero_id, {}).get("localized_name_ru", str(m.hero_id))
            print(f"  {name} (id={m.hero_id}) vs 12: adv={m.advantage}, wr={m.winrate}")

        r2 = await s.execute(select(Matchup).where(Matchup.hero_id == 12).order_by(Matchup.advantage.desc()).limit(10))
        print("\nPL (12) vs others:")
        for m in r2.scalars():
            name = HERO_BY_ID.get(m.vs_hero_id, {}).get("localized_name_ru", str(m.vs_hero_id))
            print(f"  12 vs {name} (id={m.vs_hero_id}): adv={m.advantage}, wr={m.winrate}")

        # Check total matchups count
        count_r = await s.execute(select(Matchup))
        all_m = count_r.scalars().all()
        print(f"\nTotal Matchups in DB: {len(all_m)}")

    import httpx
    try:
        r = httpx.get("https://api.opendota.com/api/heroes/12/matchups", timeout=6.0)
        if r.status_code == 200:
            data = r.json()
            print(f"\nOpenDota /heroes/12/matchups returned {len(data)} items. First 5:")
            for item in data[:5]:
                vs_id = item.get("hero_id")
                name = HERO_BY_ID.get(vs_id, {}).get("localized_name_ru", str(vs_id))
                games = item.get("games_played", 0)
                wins = item.get("wins", 0)
                wr = (wins / games) * 100.0 if games else 0
                print(f"  hero_id 12 vs {name} ({vs_id}): games={games}, wins={wins}, wr={wr:.2f}%")
    except Exception as e:
        print(f"OpenDota test error: {e}")

if __name__ == "__main__":
    asyncio.run(check())
