from __future__ import annotations

from playwright.sync_api import Page

from config.settings import Settings
from pages.base_page import BasePage


class OpenAccountPage(BasePage):
    ACCOUNT_TYPE_SELECT = "#type"
    FROM_ACCOUNT_SELECT = "#fromAccountId"
    FROM_ACCOUNT_OPTIONS = "#fromAccountId option"
    OPEN_BUTTON = "input[value='Open New Account']"
    RESULT_TITLE = "#openAccountResult .title"
    NEW_ACCOUNT_ID = "#newAccountId"

    SUCCESS_TEXT = "Account Opened!"

    CHECKING = "CHECKING"
    SAVINGS = "SAVINGS"

    def __init__(self, page: Page, settings: Settings) -> None:
        super().__init__(page, settings)

    def open_page(self) -> None:
        self.open("openaccount.htm")
        self.page.locator(self.FROM_ACCOUNT_OPTIONS).first.wait_for(
            state="attached"
        )

    def open_new_account(self, account_type: str = SAVINGS) -> None:
        self.select_option(self.ACCOUNT_TYPE_SELECT, account_type)
        self.click(self.OPEN_BUTTON)

    def is_account_opened(self) -> bool:
        return self.text_appears(self.SUCCESS_TEXT)

    def new_account_id(self) -> str:
        if self.is_visible(self.NEW_ACCOUNT_ID):
            return self.text_of(self.NEW_ACCOUNT_ID)
        return ""