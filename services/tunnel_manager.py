import asyncio
import logging
import re
import shutil
from pathlib import Path
import httpx
from config import settings

logger = logging.getLogger("tunnel_manager")

class TunnelManager:
    def __init__(self):
        self.process = None
        self._task = None
        self._running = False
        self.current_url = None

    @staticmethod
    def _is_static_cloud_https(url: str) -> bool:
        """Returns True if WEBAPP_URL is a permanent public HTTPS URL (e.g. Render, Railway, Koyeb, custom domain)."""
        if not url or not url.startswith("https://"):
            return False
        ephemeral_domains = (".lhr.life", "localhost", "127.0.0.1")
        return not any(d in url for d in ephemeral_domains)

    async def _update_telegram_menu_button(self, url: str):
        if not settings.BOT_TOKEN or ":" not in settings.BOT_TOKEN:
            return
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                await client.post(
                    f"https://api.telegram.org/bot{settings.BOT_TOKEN}/setChatMenuButton",
                    json={
                        "menu_button": {
                            "type": "web_app",
                            "text": "⚔️ Драфт",
                            "web_app": {"url": url}
                        }
                    }
                )
            logger.info(f"✅ Telegram Bot MenuButtonWebApp updated to: {url}")
        except Exception as tg_err:
            logger.warning(f"Could not update Telegram MenuButton: {tg_err}")

    async def start(self):
        """Starts the background tunnel supervisor or cloud keep-alive loop."""
        self._running = True
        if self._is_static_cloud_https(settings.WEBAPP_URL) or not settings.ENABLE_SSH_TUNNEL:
            self.current_url = settings.WEBAPP_URL
            logger.info(f"🌐 Static public HTTPS URL detected ({settings.WEBAPP_URL}). Skipping SSH tunnel.")
            await self._update_telegram_menu_button(settings.WEBAPP_URL)
            self._task = asyncio.create_task(self._cloud_keepalive_loop())
            return

        self._task = asyncio.create_task(self._run_loop())

    async def _cloud_keepalive_loop(self):
        """Periodically pings /api/health on cloud deployments to help prevent free-tier spin-down."""
        health_url = f"{settings.WEBAPP_URL.rstrip('/')}/api/health"
        while self._running:
            await asyncio.sleep(600)  # 10 minutes
            if not self._running:
                break
            try:
                async with httpx.AsyncClient(timeout=10.0) as client:
                    await client.get(health_url)
            except Exception as e:
                logger.debug(f"Keep-alive ping failed: {e}")

    async def stop(self):
        """Stops the tunnel process."""
        self._running = False
        if self.process:
            try:
                self.process.terminate()
            except Exception:
                pass
        if self._task and not self._task.done():
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass

    async def _run_loop(self):
        while self._running:
            try:
                ssh_path = shutil.which("ssh")
                if not ssh_path:
                    logger.warning("ssh binary not found, auto-tunnel disabled.")
                    return

                cmd = [
                    ssh_path,
                    "-o", "StrictHostKeyChecking=no",
                    "-o", "ServerAliveInterval=15",
                    "-o", "ServerAliveCountMax=3",
                    "-o", "ExitOnForwardFailure=yes",
                    "-R", f"80:localhost:{settings.PORT}",
                    "nokey@localhost.run"
                ]

                logger.info("Starting auto-managed SSH tunnel via localhost.run...")
                self.process = await asyncio.create_subprocess_exec(
                    *cmd,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.STDOUT
                )

                while self._running and self.process.stdout:
                    line = await self.process.stdout.readline()
                    if not line:
                        break
                    text = line.decode("utf-8", errors="ignore").strip()
                    m = re.search(r"https://([a-zA-Z0-9]+\.lhr\.life)", text)
                    if m:
                        url = m.group(0)
                        self.current_url = url
                        settings.WEBAPP_URL = url
                        logger.info(f"🚀 LIVE WEBAPP TUNNEL URL ESTABLISHED: {url}")
                        self._persist_url(url)
                        await self._update_telegram_menu_button(url)

                if self.process:
                    await self.process.wait()
                    logger.warning("SSH tunnel disconnected. Reconnecting in 3 seconds...")
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"SSH tunnel supervisor error: {e}. Reconnecting in 3 seconds...")

            if self._running:
                await asyncio.sleep(3)

    def _persist_url(self, url: str):
        try:
            env_file = Path(__file__).resolve().parent.parent / ".env"
            if env_file.exists():
                content = env_file.read_text(encoding="utf-8")
                if "WEBAPP_URL=" in content:
                    new_content = re.sub(r"WEBAPP_URL=.*", f"WEBAPP_URL={url}", content)
                else:
                    new_content = content + f"\nWEBAPP_URL={url}\n"
                env_file.write_text(new_content, encoding="utf-8")
        except Exception as e:
            logger.debug(f"Could not persist WEBAPP_URL to .env: {e}")

tunnel_manager = TunnelManager()
