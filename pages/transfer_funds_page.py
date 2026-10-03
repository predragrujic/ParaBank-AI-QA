from __future__ import annotations

from playwright.sync_api import Page

from config.settings import Settings
from pages.base_page import BasePage


class TransferFundsPage(BasePage):
    AMOUNT_INPUT = "#amount"
    FROM_ACCOUNT_SELECT = "#fromAccountId"
    TO_ACCOUNT_SELECT = "#toAccountId"
    FROM_ACCOUNT_OPTIONS = "#fromAccountId option"
    TO_ACCOUNT_OPTIONS = "#toAccountId option"
    TRANSFER_BUTTON = "input[value='Transfer']"
    ERROR_MESSAGE = ".error"

    SUCCESS_TEXT = "Transfer Complete!"

    def __init__(self, page: Page, settings: Settings) -> None:
        super().__init__(page, settings)

    def open_page(self) -> None:
        self.open("transfer.htm")
        self.page.locator(self.FROM_ACCOUNT_OPTIONS).first.wait_for(
            state="attached"
        )
        self.page.locator(self.TO_ACCOUNT_OPTIONS).first.wait_for(
            state="attached"
        )

    def transfer(
        self,
        amount: str,
        from_account: str | None = None,
        to_account: str | None = None,
    ) -> None:
        self.fill(self.AMOUNT_INPUT, amount)
        if from_account:
            self.select_option(self.FROM_ACCOUNT_SELECT, from_account)
        if to_account:
            self.select_option(self.TO_ACCOUNT_SELECT, to_account)
        self.click(self.TRANSFER_BUTTON)

    def is_transfer_complete(self) -> bool:
        return self.text_appears(self.SUCCESS_TEXT)

    def error_message(self) -> str:
        if self.is_visible(self.ERROR_MESSAGE):
            return self.text_of(self.ERROR_MESSAGE)
        return ""