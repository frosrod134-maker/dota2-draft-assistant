import asyncio
import logging
from contextlib import asynccontextmanager
from typing import Optional, Union, Any
from pathlib import Path

from fastapi import FastAPI, Depends, BackgroundTasks, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

import httpx
from config import settings, BASE_DIR
from database.db import init_db, get_db, AsyncSessionLocal
from database.models import Hero, RoleStat, Matchup
from services.scraper.seed_data import seed_database
from services.scraper.d2pt_scraper import d2pt_scraper
from services.scraper.dotabuff_scraper import dotabuff_scraper
from services.draft_engine import draft_engine
from services.tunnel_manager import tunnel_manager
from services.hero_roles import HERO_VIABLE_ROLES, HERO_PRIMARY_ROLE
from bot.handlers import router as bot_router

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("main")

bot: Optional[Bot] = None
dp: Optional[Dispatcher] = None
bot_task: Optional[asyncio.Task] = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    # ── 1. STARTUP ──
    logger.info("Initializing database...")
    await init_db()

    # Seed initial data if enabled
    if settings.AUTO_SEED_ON_STARTUP:
        async with AsyncSessionLocal() as session:
            await seed_database(session)

    # ── 2. START AIOGRAM BOT (CONCURRENTLY) ──
    global bot, dp, bot_task
    token = settings.BOT_TOKEN.strip()
    # Check if a valid token format is provided (digits:alphanumeric)
    if token and ":" in token and not token.startswith("1234567890"):
        try:
            logger.info("Starting Telegram Bot via aiogram 3...")
            bot = Bot(token=token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
            dp = Dispatcher()
            dp.include_router(bot_router)

            # Delete webhook and drop pending updates on startup
            await bot.delete_webhook(drop_pending_updates=True)

            # Launch polling in background task so FastAPI is not blocked
            async def run_bot_polling():
                try:
                    logger.info("aiogram 3 bot polling started.")
                    await dp.start_polling(bot)
                except asyncio.CancelledError:
                    logger.info("aiogram 3 bot polling task cancelled.")
                except Exception as e:
                    logger.error(f"Telegram bot polling encountered error: {e}")

            bot_task = asyncio.create_task(run_bot_polling())
        except Exception as e:
            logger.warning(f"Could not start Telegram Bot (check BOT_TOKEN in .env): {e}")
    else:
        logger.info(
            "Telegram BOT_TOKEN is not set or using default example. "
            "FastAPI and WebApp run fully functional in standalone mode!"
        )

    # ── 3. AUTO-MANAGED HTTPS TUNNEL ──
    # Starts background tunnel if no custom static domain is set
    logger.info("Starting auto-managed HTTPS tunnel...")
    await tunnel_manager.start()

    yield

    # ── 4. SHUTDOWN ──
    logger.info("Shutting down services...")
    await tunnel_manager.stop()
    if bot_task and not bot_task.done():
        bot_task.cancel()
        try:
            await bot_task
        except asyncio.CancelledError:
            pass

    if bot:
        await bot.session.close()
    logger.info("Shutdown completed.")

app = FastAPI(
    title="Dota 2 Draft Assistant",
    description="Mathematical Counter-Pick & Synergy Engine with D2PT Meta stats and Telegram Mini App",
    version="1.0.0",
    lifespan=lifespan
)

# Static files
static_dir = BASE_DIR / "static"
static_dir.mkdir(parents=True, exist_ok=True)
app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

@app.middleware("http")
async def disable_client_cache(request, call_next):
    response = await call_next(request)
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

from services.hero_guides import get_team_counter_items, generate_hero_guide
from services.aliases import search_heroes

def parse_hero_id(val: Any) -> Optional[int]:
    if isinstance(val, int):
        return val
    s = str(val).strip()
    if s.isdigit():
        return int(s)
    matches = search_heroes(s)
    if matches:
        return matches[0]["id"]
    return None

# ── REQUEST SCHEMAS ──
class RecommendRequest(BaseModel):
    ally_ids: list[Any] = Field(default=[], description="Hero IDs or names picked by user's team")
    enemy_ids: list[Any] = Field(default=[], description="Hero IDs or names picked by enemy team")
    allies: Optional[list[Any]] = None
    enemies: Optional[list[Any]] = None
    role: Optional[Union[int, str]] = Field(default=None, description="Position (1: Carry, 2: Mid, 3: Offlane, 4: Soft, 5: Hard) or 'any'")
    top_k: int = Field(default=20, ge=1, le=50, description="Number of recommendations to return")

    def get_allies(self) -> list[int]:
        raw = self.allies if self.allies is not None else self.ally_ids
        ids = []
        for x in raw:
            hid = parse_hero_id(x)
            if hid is not None:
                ids.append(hid)
        return ids

    def get_enemies(self) -> list[int]:
        raw = self.enemies if self.enemies is not None else self.enemy_ids
        ids = []
        for x in raw:
            hid = parse_hero_id(x)
            if hid is not None:
                ids.append(hid)
        return ids

    def get_role(self) -> Optional[int]:
        if self.role in (None, "", "any", "all", "none"):
            return None
        try:
            return int(self.role)
        except (ValueError, TypeError):
            return None

# ── API ENDPOINTS ──

@app.get("/", include_in_schema=False)
async def serve_index():
    """Serves the Telegram Mini App / Web frontend."""
    index_path = static_dir / "index.html"
    if index_path.exists():
        return FileResponse(index_path)
    return JSONResponse({"status": "ok", "message": "Draft Assistant API is running."})

@app.get("/api/heroes")
async def get_heroes(db: AsyncSession = Depends(get_db)):
    """Returns all heroes with localized names, roles, icons, aliases, and meta stats, sorted A-Z by English name."""
    result = await db.execute(select(Hero).order_by(Hero.localized_name.asc()))
    heroes = result.scalars().all()

    # Pre-fetch top role stats for winrate display
    rs_res = await db.execute(select(RoleStat).order_by(RoleStat.matches.desc()))
    rs_list = rs_res.scalars().all()
    winrate_map = {}
    for rs in rs_list:
        if rs.hero_id not in winrate_map:
            winrate_map[rs.hero_id] = (round(rs.winrate, 1), rs.tier)

    out = []
    for h in heroes:
        d = h.to_dict()
        wr, tier = winrate_map.get(h.id, (50.0, "B"))
        d["winrate"] = wr
        d["tier"] = tier
        d["viable_roles"] = HERO_VIABLE_ROLES.get(h.id, [])
        d["primary_role"] = HERO_PRIMARY_ROLE.get(h.id, 3)
        out.append(d)
    return out

@app.get("/api/heroes/{hero_id}/guide")
async def get_hero_guide(hero_id: int, db: AsyncSession = Depends(get_db)):
    """
    Returns rich Russian tactical guide, counter items, hard counters,
    strong against, best synergies, and tips for the given hero.
    """
    guide = await generate_hero_guide(db, hero_id)
    if "error" in guide:
        return JSONResponse({"status": "error", "message": guide["error"]}, status_code=404)
    return {"status": "success", "guide": guide}

@app.post("/api/recommend")
async def get_recommendations(
    req: RecommendRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Computes real-time draft recommendations based on current allies,
    enemies, and target position with situational and meta classification.
    """
    allies = req.get_allies()
    enemies = req.get_enemies()
    parsed_role = req.get_role()
    recommendations = await draft_engine.recommend(
        db_session=db,
        ally_ids=allies,
        enemy_ids=enemies,
        role=parsed_role,
        top_k=req.top_k
    )
    team_items = get_team_counter_items(enemies)
    return {
        "status": "success",
        "total": len(recommendations),
        "role": parsed_role,
        "recommendations": recommendations,
        "team_counter_items": team_items
    }

@app.post("/api/sync")
async def sync_data(
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db)
):
    """
    Triggers an asynchronous scrape and refresh of D2PT & Dotabuff data.
    """
    async def perform_sync():
        async with AsyncSessionLocal() as session:
            try:
                await d2pt_scraper.sync_d2pt(session)
                await dotabuff_scraper.sync_top_heroes(session, limit=10)
            except Exception as e:
                logger.error(f"Background sync failed: {e}")

    background_tasks.add_task(perform_sync)
    return {"status": "ok", "message": "Background sync scheduled successfully."}

cached_patch_info = {
    "patch": "Патч 7.41f",
    "raw_patch": "7.41f",
    "status": "Live D2PT & OpenDota"
}

@app.get("/api/patch")
async def get_patch_info():
    """Returns current live Dota 2 patch with fallback."""
    global cached_patch_info
    try:
        async with httpx.AsyncClient(timeout=3.0) as client:
            resp = await client.get(f"{settings.OPENDOTA_API_URL}/constants/patch")
            if resp.status_code == 200:
                patches = resp.json()
                if isinstance(patches, list) and len(patches) > 0:
                    latest = patches[-1]
                    name = latest.get("name", "7.41f")
                    # If OpenDota is lagging behind current active patch 7.41f, ensure 7.41f
                    if name < "7.41f":
                        name = "7.41f"
                    cached_patch_info = {
                        "patch": f"Патч {name}",
                        "raw_patch": name,
                        "date": latest.get("date", ""),
                        "status": "Live D2PT & OpenDota"
                    }
    except Exception as e:
        logger.warning(f"Could not refresh patch info: {e}")
    return cached_patch_info

@app.get("/api/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "dota2-draft-assistant"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=False
    )
