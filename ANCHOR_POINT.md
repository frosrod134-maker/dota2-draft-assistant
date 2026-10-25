# ANCHOR_POINT.md
> **FUTURE AGENTS: Read ANCHOR_POINT.md first. Do NOT scan the full repository. Jump directly to the file listed in the map.**

## Project Stack & Entrypoint Summary
- **Project Name:** Dota 2 Draft Assistant & Encyclopedia
- **Patch Baseline:** Dota 2 Patch 7.41f
- **Backend:** FastAPI (Python 3.12, Async SQLAlchemy, SQLite `database/dota_draft.db`, aiosqlite)
- **Telegram Bot:** Aiogram 3.x (Web App integration & command router)
- **Frontend:** Pure HTML5/ES6 / Tailwind CSS / Vanilla JS (`static/index.html`, `static/app.js`)
- **Main Entrypoint:** `main.py` (FastAPI app, lifespan manager, `/api/heroes`, `/api/heroes/{id}/guide`, `/api/recommend`)

---

## Exact File Map & Line-by-Line Responsibility

| File Path | Core Responsibility |
|---|---|
| `main.py` | FastAPI application, lifespan startup/shutdown, router attachments, static file hosting, REST endpoints. |
| `config.py` | Environment configurations (`pydantic-settings`), token loading, default host/port definitions. |
| `requirements.txt` | Python runtime dependencies. |
| `README.md` | General overview and project documentation. |
| `bot/handlers.py` | Aiogram 3 handlers for `/start`, `/draft`, `/heroes`, inline queries and WebApp buttons. |
| `database/db.py` | Async engine and session factory (`AsyncSessionLocal`, `init_db`). |
| `database/models.py` | Declarative SQLAlchemy models: `Hero`, `RoleStat`, `Matchup`. |
| `services/aliases.py` | Canonical list of 126 Valve heroes, Russian localized names, search aliases, attribute mappings. |
| `services/hero_roles.py` | `HERO_VIABLE_ROLES`, `HERO_PRIMARY_ROLE`, and `HARD_CARRIES` maps for positions 1-5. |
| `services/draft_engine.py` | Draft recommendation algorithm: synergy, counter advantage, role filtering, team balance. |
| `services/hero_guides.py` | Tactical hero guides, counter-items catalog, curated profiles (12, 14, 44, 59, 82, 93, 94, 99). |
| `services/tunnel_manager.py` | Automatic background SSH tunnel to localhost.run & auto-update Telegram bot `setChatMenuButton`. |
| `services/scraper/d2pt_scraper.py` | Dota2ProTracker scraper for meta winrates and role statistics. |
| `services/scraper/dotabuff_scraper.py` | OpenDota/Dotabuff pairwise matchup fetcher with dynamic `base_wr` and `CURATED_MATCHUPS` protection. |
| `services/scraper/seed_data.py` | Database seeder with baseline role stats, matchups, and in-place hero name synchronization. |
| `static/index.html` | SPA layout with Draft View, Wiki View, Guide Modal, and Telegram WebApp integration. |
| `static/app.js` | SPA logic: draft slot selection, recommendation filters, wiki role filtering, interactive guides. |

---

## Verification & Working State
- **State Hash / Timestamp:** `2026-10-19 13:58:00 UTC+5`
- **Integrity Status:** Verified 0 circular imports, 0 missing role IDs, 0 banned typos, 0 mutual exclusion overlaps in guide recommendations.
