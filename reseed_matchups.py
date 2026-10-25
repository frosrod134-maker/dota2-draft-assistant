import asyncio
import sys
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

from database.db import AsyncSessionLocal
from database.models import Matchup
from services.scraper.seed_data import BASELINE_MATCHUPS
from sqlalchemy import select, delete

async def reseed():
    async with AsyncSessionLocal() as session:
        # Delete old matchups and insert fresh BASELINE_MATCHUPS
        await session.execute(delete(Matchup))
        for hero_a, hero_b, adv, syn in BASELINE_MATCHUPS:
            session.add(Matchup(
                hero_id=hero_a,
                vs_hero_id=hero_b,
                advantage=adv,
                winrate=50.0 + (adv * 1.5),
                synergy=syn
            ))
            session.add(Matchup(
                hero_id=hero_b,
                vs_hero_id=hero_a,
                advantage=-adv,
                winrate=50.0 - (adv * 1.5),
                synergy=syn
            ))
        await session.commit()
        
        count = (await session.execute(select(Matchup))).scalars().all()
        print(f"Reseeded {len(count)} matchups into database successfully.")

if __name__ == "__main__":
    asyncio.run(reseed())
