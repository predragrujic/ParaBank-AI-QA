from __future__ import annotations

from contextlib import suppress
from pathlib import Path
from types import TracebackType

from playwright.sync_api import (
    Browser,
    BrowserContext,
    Page,
    Playwright,
    ViewportSize,
    sync_playwright,
)
from playwright.sync_api import Error as PlaywrightError

from config.settings import Settings


class BrowserManager:

    def __init__(self, settings: Settings) -> None:
        self._settings = settings
        self._playwright: Playwright | None = None
        self._browser: Browser | None = None
        self._context: BrowserContext | None = None
        self._page: Page | None = None


    def start(self) -> Page:
        if self._page is not None:
            return self._page

        self._playwright = sync_playwright().start()
        self._browser = self._playwright.chromium.launch(
            headless=self._settings.headless,
            slow_mo=self._settings.slow_mo_ms,
        )
        self._context = self._browser.new_context(
            viewport=ViewportSize(
                width=self._settings.viewport_width,
                height=self._settings.viewport_height,
            )
        )
        self._context.set_default_timeout(self._settings.default_timeout_ms)
        self._page = self._context.new_page()
        return self._page

    def stop(self) -> None:
        if self._context is not None:
            with suppress(PlaywrightError):
                self._context.close()
        if self._browser is not None:
            with suppress(PlaywrightError):
                self._browser.close()
        if self._playwright is not None:
            with suppress(PlaywrightError):
                self._playwright.stop()

        self._page = None
        self._context = None
        self._browser = None
        self._playwright = None


    def __enter__(self) -> BrowserManager:
        self.start()
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        self.stop()


    @property
    def page(self) -> Page:
        if self._page is None:
            raise RuntimeError("Browser is not started. Call start() first.")
        return self._page

    def reset_session(self) -> None:
        if self._context is None:
            raise RuntimeError("Browser is not started. Call start() first.")
        self._context.clear_cookies()
        self.page.goto(self._settings.home_url)

    def take_screenshot(self, name: str) -> Path:
        path = self._settings.screenshots_dir / f"{name}.png"
        self.page.screenshot(path=str(path), full_page=True)
        return path