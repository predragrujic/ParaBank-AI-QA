from __future__ import annotations

from playwright.sync_api import Page, expect

from config.settings import Settings
from pages.base_page import BasePage


class UpdateProfilePage(BasePage):
    FIRST_NAME = "input[id='customer.firstName']"
    LAST_NAME = "input[id='customer.lastName']"
    STREET = "input[id='customer.address.street']"
    CITY = "input[id='customer.address.city']"
    STATE = "input[id='customer.address.state']"
    ZIP_CODE = "input[id='customer.address.zipCode']"
    PHONE = "input[id='customer.phoneNumber']"
    UPDATE_BUTTON = "input[value='Update Profile']"
    ERRORS = ".error"

    SUCCESS_TEXT = "Profile Updated"

    def __init__(self, page: Page, settings: Settings) -> None:
        super().__init__(page, settings)

    def open_page(self) -> None:
        self.open("updateprofile.htm")
        expect(self.page.locator(self.FIRST_NAME)).not_to_have_value("")

    def update_contact_info(
        self,
        street: str | None = None,
        city: str | None = None,
        state: str | None = None,
        zip_code: str | None = None,
        phone: str | None = None,
    ) -> None:
        updates = {
            self.STREET: street,
            self.CITY: city,
            self.STATE: state,
            self.ZIP_CODE: zip_code,
            self.PHONE: phone,
        }
        for selector, value in updates.items():
            if value is not None:
                self.fill(selector, value)
        self.click(self.UPDATE_BUTTON)

    def is_profile_updated(self) -> bool:
        return self.text_appears(self.SUCCESS_TEXT)

    def error_messages(self) -> list[str]:
        if not self.is_visible(self.ERRORS):
            return []
        texts = self.page.locator(self.ERRORS).all_inner_texts()
        return [text.strip() for text in texts if text.strip()]