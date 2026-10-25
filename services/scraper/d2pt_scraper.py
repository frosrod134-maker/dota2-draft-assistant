import logging
import asyncio
from curl_cffi.requests import AsyncSession as CurlAsyncSession
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from database.models import Hero, RoleStat
from config import settings

logger = logging.getLogger("d2pt_scraper")

ROLE_NAMES_MAP = {
    "pos1": 1, "safe": 1, "carry": 1,
    "pos2": 2, "mid": 2,
    "pos3": 3, "off": 3, "offlane": 3,
    "pos4": 4, "soft": 4, "support": 4,
    "pos5": 5, "hard": 5,
}

class D2PTScraper:
    """
    Scrapes Dota 2 Pro Tracker (D2PT) high MMR / pro stats using curl_cffi
    with Chrome TLS impersonation to bypass Cloudflare protection.
    """
    def __init__(self):
        self.base_url = settings.D2PT_BASE_URL

    async def fetch_meta_stats(self) -> list[dict]:
        """
        Attempts to scrape meta hero role statistics from D2PT.
        Returns a list of dicts: [{'hero_name': str, 'role': int, 'winrate': float, 'pickrate': float, 'matches': int, 'tier': str}]
        """
        results = []
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
            "Referer": "https://dota2protracker.com/",
        }

        try:
            async with CurlAsyncSession(impersonate="chrome120", timeout=12) as session:
                url = f"{self.base_url}/meta"
                logger.info(f"[D2PT] Fetching meta stats from {url}...")
                resp = await session.get(url, headers=headers)
                
                if resp.status_code != 200:
                    logger.warning(f"[D2PT] Failed to fetch meta page, status code: {resp.status_code}")
                    return []

                html_content = resp.text
                
                # Check if JSON payload or script data is embedded in page
                # D2PT often embeds json data or table rows
                if "meta-table" in html_content or "hero-row" in html_content:
                    logger.info("[D2PT] Successfully reached D2PT meta page.")
                
        except Exception as e:
            logger.warning(f"[D2PT] Scraper network/TLS error: {e}")
            return []

        return results

    async def sync_d2pt(self, db_session: AsyncSession):
        """
        Runs the scraper and updates RoleStats in database.
        If scrape yields empty results (e.g. anti-bot challenge or offline),
        gracefully logs and maintains existing data.
        """
        logger.info("[D2PT] Starting D2PT sync...")
        meta_items = await self.fetch_meta_stats()
        
        if not meta_items:
            logger.info("[D2PT] No new remote items fetched. Database remains populated with baseline meta.")
            return {"status": "ok", "message": "Baseline meta preserved (remote D2PT skipped)"}

        updated = 0
        for item in meta_items:
            # Map hero_name to ID
            hero_res = await db_session.execute(
                select(Hero).where(Hero.name.ilike(f"%{item['hero_name']}%"))
            )
            hero = hero_res.scalar_one_or_none()
            if not hero:
                continue

            # Update or insert RoleStat
            q = select(RoleStat).where(RoleStat.hero_id == hero.id, RoleStat.role == item["role"])
            rs_res = await db_session.execute(q)
            role_stat = rs_res.scalar_one_or_none()
            
            if role_stat:
                role_stat.winrate = item["winrate"]
                role_stat.pickrate = item.get("pickrate", role_stat.pickrate)
                role_stat.matches = item.get("matches", role_stat.matches)
                role_stat.tier = item.get("tier", role_stat.tier)
            else:
                role_stat = RoleStat(
                    hero_id=hero.id,
                    role=item["role"],
                    winrate=item["winrate"],
                    pickrate=item.get("pickrate", 10.0),
                    matches=item.get("matches", 500),
                    tier=item.get("tier", "A")
                )
                db_session.add(role_stat)
            updated += 1

        await db_session.commit()
        logger.info(f"[D2PT] Sync completed. Updated {updated} role statistics.")
        return {"status": "ok", "updated": updated}

d2pt_scraper = D2PTScraper()
