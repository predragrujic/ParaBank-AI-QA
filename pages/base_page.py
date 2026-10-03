from __future__ import annotations

from playwright.sync_api import Page
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

from config.settings import Settings


class BasePage:
    def __init__(self, page: Page, settings: Settings) -> None:
        self.page = page
        self.settings = settings

    def open(self, path: str = "index.htm") -> None:
        self.page.goto(f"{self.settings.base_url}/{path.lstrip('/')}")

    def click_link(self, name: str) -> None:
        self.page.get_by_role("link", name=name, exact=True).first.click()

    @property
    def current_url(self) -> str:
        return self.page.url

    @property
    def title(self) -> str:
        return self.page.title()

    def click(self, selector: str) -> None:
        self.page.locator(selector).first.click()

    def fill(self, selector: str, value: str) -> None:
        self.page.locator(selector).first.fill(value)

    def select_option(self, selector: str, value: str) -> None:
        self.page.locator(selector).first.select_option(value)

    def text_of(self, selector: str) -> str:
        return self.page.locator(selector).first.inner_text().strip()

    def page_text(self) -> str:
        return self.page.locator("body").inner_text()

    def is_visible(self, selector: str, timeout_ms: int = 3_000) -> bool:
        try:
            self.page.locator(selector).first.wait_for(
                state="visible", timeout=timeout_ms
            )
            return True
        except PlaywrightTimeoutError:
            return False

    def text_appears(self, text: str, timeout_ms: int = 5_000) -> bool:
        try:
            self.page.get_by_text(text, exact=False).first.wait_for(
                state="visible", timeout=timeout_ms
            )
            return True
        except PlaywrightTimeoutError:
            return False