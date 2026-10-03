from __future__ import annotations

from playwright.sync_api import Page

from config.settings import Settings
from pages.base_page import BasePage


class LoginPage(BasePage):
    USERNAME_INPUT = "input[name='username']"
    PASSWORD_INPUT = "input[name='password']"
    LOGIN_BUTTON = "input[value='Log In']"
    ERROR_MESSAGE = "p.error"

    LOGIN_PANEL_TEXT = "Customer Login"
    OVERVIEW_HEADING_TEXT = "Accounts Overview"
    LOGOUT_LINK_TEXT = "Log Out"

    def __init__(self, page: Page, settings: Settings) -> None:
        super().__init__(page, settings)

    def open_login(self) -> None:
        self.open("index.htm")

    def login(self, username: str, password: str) -> None:
        self.fill(self.USERNAME_INPUT, username)
        self.fill(self.PASSWORD_INPUT, password)
        self.click(self.LOGIN_BUTTON)

    def logout(self) -> None:
        self.click_link(self.LOGOUT_LINK_TEXT)

    def is_login_form_displayed(self) -> bool:
        return self.text_appears(self.LOGIN_PANEL_TEXT)

    def is_logged_in(self) -> bool:
        return self.text_appears(self.OVERVIEW_HEADING_TEXT)

    def error_message(self) -> str:
        if self.is_visible(self.ERROR_MESSAGE):
            return self.text_of(self.ERROR_MESSAGE)
        return ""