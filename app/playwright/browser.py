from pathlib import Path
from typing import Any

from playwright.async_api import BrowserContext, Page, async_playwright

from app.config.settings import get_settings


class BrowserAutomation:
    def __init__(self) -> None:
        config = get_settings().yaml_config.get("browser", {})
        self.headless = bool(config.get("headless", False))
        self.storage_dir = Path(config.get("storage_dir", "browser-data"))
        self.screenshot_dir = Path(config.get("screenshot_dir", "screenshots"))
        self.timeout_ms = int(config.get("timeout_ms", 30000))

    async def __aenter__(self) -> "BrowserAutomation":
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        self.screenshot_dir.mkdir(parents=True, exist_ok=True)
        self.playwright = await async_playwright().start()
        self.context = await self.playwright.chromium.launch_persistent_context(
            user_data_dir=str(self.storage_dir),
            headless=self.headless,
            timeout=self.timeout_ms,
        )
        return self

    async def __aexit__(self, exc_type: Any, exc: Any, tb: Any) -> None:
        await self.context.close()
        await self.playwright.stop()

    async def new_page(self) -> Page:
        page = await self.context.new_page()
        page.set_default_timeout(self.timeout_ms)
        return page

    async def screenshot(self, page: Page, name: str) -> str:
        path = self.screenshot_dir / f"{name}.png"
        await page.screenshot(path=str(path), full_page=True)
        return str(path)

