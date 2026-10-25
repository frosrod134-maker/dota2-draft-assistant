import logging
import asyncio
from curl_cffi.requests import AsyncSession as CurlAsyncSession
import httpx
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from database.models import Matchup, Hero
from config import settings
from services.draft_engine import CURATED_MATCHUPS

logger = logging.getLogger("dotabuff_scraper")

class DotabuffScraper:
    """
    Scrapes or synchronizes hero matchups and counter advantages.
    Uses OpenDota matchup endpoint and Dotabuff with curl_cffi.
    """
    def __init__(self):
        self.base_url = settings.DOTABUFF_BASE_URL
        self.opendota_url = settings.OPENDOTA_API_URL

    async def fetch_opendota_matchups(self, hero_id: int) -> list[dict]:
        """
        Fetches official pairwise matchups for a hero from OpenDota API.
        Applies Bayesian smoothing with C=40 matches to prevent sample size distortion.
        Returns list of {'vs_hero_id': int, 'games_played': int, 'hero_adv': float, 'hero_wr': float, 'vs_adv': float, 'vs_wr': float}
        """
        url = f"{self.opendota_url}/heroes/{hero_id}/matchups"
        try:
            async with httpx.AsyncClient(timeout=8.0) as client:
                resp = await client.get(url)
                if resp.status_code == 200:
                    data = resp.json()
                    matchups = []
                    valid_items = [item for item in data if item.get("games_played", 0) >= 5 and item.get("hero_id")]
                    total_wins = sum(item.get("wins", 0) for item in valid_items)
                    total_games = sum(item.get("games_played", 0) for item in valid_items)
                    base_wr = (total_wins / total_games) if total_games > 0 else 0.50

                    for item in valid_items:
                        games = item.get("games_played", 0)
                        wins = item.get("wins", 0)
                        vs_id = item.get("hero_id")

                        # Bayesian smoothing towards base_wr
                        hero_wr = (wins + 25.0 * base_wr) / (games + 25.0)
                        hero_adv = (hero_wr - base_wr) * 100.0
                        if games < 30:
                            # Heavily dampen when games_played < 30
                            hero_adv *= (games / 30.0) ** 2
                        hero_adv = round(hero_adv, 2)

                        # Reciprocal for vs_id vs hero_id
                        vs_wins = games - wins
                        vs_base_wr = 1.0 - base_wr
                        vs_wr = (vs_wins + 25.0 * vs_base_wr) / (games + 25.0)
                        vs_adv = (vs_wr - vs_base_wr) * 100.0
                        if games < 30:
                            vs_adv *= (games / 30.0) ** 2
                        vs_adv = round(vs_adv, 2)

                        matchups.append({
                            "vs_hero_id": vs_id,
                            "games_played": games,
                            "hero_adv": hero_adv,
                            "hero_wr": round(hero_wr * 100.0, 2),
                            "vs_adv": vs_adv,
                            "vs_wr": round(vs_wr * 100.0, 2),
                        })
                    return matchups
        except Exception as e:
            logger.warning(f"[Dotabuff/OpenDota] Error fetching matchups for hero {hero_id}: {e}")
        return []

    async def sync_hero_matchups(self, hero_id: int, db_session: AsyncSession):
        """
        Syncs matchups for a specific hero into database, saving reciprocal pairs.
        Skips overwriting pairs defined in CURATED_MATCHUPS.
        """
        matchups = await self.fetch_opendota_matchups(hero_id)
        if not matchups:
            return 0

        count = 0
        for m in matchups:
            vs_id = m["vs_hero_id"]
            
            # 1. hero_id vs vs_id
            if (hero_id, vs_id) not in CURATED_MATCHUPS:
                q1 = select(Matchup).where(Matchup.hero_id == hero_id, Matchup.vs_hero_id == vs_id)
                res1 = await db_session.execute(q1)
                ex1 = res1.scalar_one_or_none()
                if ex1:
                    ex1.advantage = m["hero_adv"]
                    ex1.winrate = m["hero_wr"]
                    ex1.games_played = m["games_played"]
                else:
                    db_session.add(Matchup(
                        hero_id=hero_id,
                        vs_hero_id=vs_id,
                        advantage=m["hero_adv"],
                        winrate=m["hero_wr"],
                        games_played=m["games_played"],
                        synergy=0.0
                    ))

            # 2. Reciprocal: vs_id vs hero_id
            if (vs_id, hero_id) not in CURATED_MATCHUPS:
                q2 = select(Matchup).where(Matchup.hero_id == vs_id, Matchup.vs_hero_id == hero_id)
                res2 = await db_session.execute(q2)
                ex2 = res2.scalar_one_or_none()
                if ex2:
                    ex2.advantage = m["vs_adv"]
                    ex2.winrate = m["vs_wr"]
                    ex2.games_played = m["games_played"]
                else:
                    db_session.add(Matchup(
                        hero_id=vs_id,
                        vs_hero_id=hero_id,
                        advantage=m["vs_adv"],
                        winrate=m["vs_wr"],
                        games_played=m["games_played"],
                        synergy=0.0
                    ))
            count += 1
        await db_session.commit()
        return count

    async def sync_top_heroes(self, db_session: AsyncSession, limit: int = 15):
        """
        Syncs matchups for the most popular meta heroes to prevent rate limits.
        """
        logger.info(f"[Dotabuff] Syncing matchups for top {limit} heroes...")
        heroes_res = await db_session.execute(select(Hero.id).limit(limit))
        hero_ids = heroes_res.scalars().all()
        
        total = 0
        for hid in hero_ids:
            synced = await self.sync_hero_matchups(hid, db_session)
            total += synced
            await asyncio.sleep(0.5)  # Rate limit courtesy
            
        logger.info(f"[Dotabuff] Matchup sync complete. Updated {total} matchups.")
        return {"status": "ok", "synced_records": total}

dotabuff_scraper = DotabuffScraper()
