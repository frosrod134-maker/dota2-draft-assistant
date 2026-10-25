import os
from pydantic_settings import BaseSettings
from pydantic import Field
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

class Settings(BaseSettings):
    BOT_TOKEN: str = Field(default="", description="Telegram Bot Token from @BotFather")
    WEBAPP_URL: str = Field(default="http://localhost:8000", description="Public or local WebApp URL")
    HOST: str = Field(default="0.0.0.0", description="FastAPI bind host")
    PORT: int = Field(default=8000, description="FastAPI bind port")
    DATABASE_URL: str = Field(
        default=f"sqlite+aiosqlite:///{BASE_DIR / 'database' / 'dota_draft.db'}",
        description="Async SQLite database URL"
    )
    OPENDOTA_API_URL: str = "https://api.opendota.com/api"
    D2PT_BASE_URL: str = "https://dota2protracker.com"
    DOTABUFF_BASE_URL: str = "https://www.dotabuff.com"
    AUTO_SEED_ON_STARTUP: bool = True
    ENABLE_SSH_TUNNEL: bool = Field(
        default=True,
        description="Enable localhost.run SSH tunnel when no static public HTTPS URL is configured"
    )
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"

settings = Settings()

# Auto-detect public HTTPS URL on cloud platforms (Render, Railway, Koyeb)
_render_url = os.getenv("RENDER_EXTERNAL_URL", "").strip()
_railway_domain = os.getenv("RAILWAY_PUBLIC_DOMAIN", "").strip()
_koyeb_domain = os.getenv("KOYEB_PUBLIC_DOMAIN", "").strip()

if _render_url:
    settings.WEBAPP_URL = _render_url.rstrip("/")
elif _railway_domain:
    settings.WEBAPP_URL = f"https://{_railway_domain.rstrip('/')}"
elif _koyeb_domain:
    settings.WEBAPP_URL = f"https://{_koyeb_domain.rstrip('/')}"

