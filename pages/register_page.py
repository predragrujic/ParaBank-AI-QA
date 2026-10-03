from __future__ import annotations

import uuid
from dataclasses import dataclass, field

from playwright.sync_api import Page

from config.settings import Settings
from pages.base_page import BasePage


def _unique_username() -> str:
    return f"qa_{uuid.uuid4().hex[:8]}"


@dataclass
class RegistrationData:
    first_name: str = "John"
    last_name: str = "Tester"
    street: str = "123 Main Street"
    city: str = "Belgrade"
    state: str = "Central Serbia"
    zip_code: str = "11000"
    phone: str = "0601234567"
    ssn: str = "123-45-6789"
    username: str = field(default_factory=_unique_username)
    password: str = "Test1234!"
    confirm_password: str = "Test1234!"


class RegisterPage(BasePage):
    FIRST_NAME = "input[id='customer.firstName']"
    LAST_NAME = "input[id='customer.lastName']"
    STREET = "input[id='customer.address.street']"
    CITY = "input[id='customer.address.city']"
    STATE = "input[id='customer.address.state']"
    ZIP_CODE = "input[id='customer.address.zipCode']"
    PHONE = "input[id='customer.phoneNumber']"
    SSN = "input[id='customer.ssn']"
    USERNAME = "input[id='customer.username']"
    PASSWORD = "input[id='customer.password']"
    CONFIRM_PASSWORD = "input[id='repeatedPassword']"
    REGISTER_BUTTON = "input[value='Register']"
    ERRORS = ".error"

    SUCCESS_TEXT = "Your account was created successfully"

    def __init__(self, page: Page, settings: Settings) -> None:
        super().__init__(page, settings)

    def open_register(self) -> None:
        self.open("register.htm")

    def fill_form(self, data: RegistrationData) -> None:
        self.fill(self.FIRST_NAME, data.first_name)
        self.fill(self.LAST_NAME, data.last_name)
        self.fill(self.STREET, data.street)
        self.fill(self.CITY, data.city)
        self.fill(self.STATE, data.state)
        self.fill(self.ZIP_CODE, data.zip_code)
        self.fill(self.PHONE, data.phone)
        self.fill(self.SSN, data.ssn)
        self.fill(self.USERNAME, data.username)
        self.fill(self.PASSWORD, data.password)
        self.fill(self.CONFIRM_PASSWORD, data.confirm_password)

    def submit(self) -> None:
        self.click(self.REGISTER_BUTTON)

    def register(self, data: RegistrationData) -> None:
        self.open_register()
        self.fill_form(data)
        self.submit()

    def is_registered_successfully(self) -> bool:
        return self.text_appears(self.SUCCESS_TEXT)

    def error_messages(self) -> list[str]:
        if not self.is_visible(self.ERRORS):
            return []
        texts = self.page.locator(self.ERRORS).all_inner_texts()
        return [text.strip() for text in texts if text.strip()]

    def has_error_containing(self, expected: str) -> bool:
        return any(
            expected.lower() in message.lower()
            for message in self.error_messages()
        )