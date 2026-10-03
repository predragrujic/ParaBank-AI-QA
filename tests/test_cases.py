from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field
from enum import Enum

from playwright.sync_api import Page

from config.settings import Settings
from pages.login_page import LoginPage
from pages.open_account_page import OpenAccountPage
from pages.register_page import RegisterPage, RegistrationData
from pages.transfer_funds_page import TransferFundsPage
from pages.update_profile_page import UpdateProfilePage


class TestType(str, Enum):
    __test__ = False

    POSITIVE = "Positive"
    NEGATIVE = "Negative"


@dataclass
class TestContext:
    __test__ = False

    settings: Settings
    login: LoginPage
    register: RegisterPage
    open_account: OpenAccountPage
    transfer: TransferFundsPage
    profile: UpdateProfilePage

    @classmethod
    def create(cls, page: Page, settings: Settings) -> TestContext:
        return cls(
            settings=settings,
            login=LoginPage(page, settings),
            register=RegisterPage(page, settings),
            open_account=OpenAccountPage(page, settings),
            transfer=TransferFundsPage(page, settings),
            profile=UpdateProfilePage(page, settings),
        )

    def register_new_user(self) -> RegistrationData:
        data = RegistrationData()
        self.register.register(data)
        _check(
            self.register.is_registered_successfully(),
            "Precondition failed: could not register a new user.",
        )
        return data


@dataclass
class TestCase:
    __test__ = False

    case_id: str
    title: str
    test_type: TestType
    preconditions: str
    steps: list[str]
    expected_result: str
    execute: Callable[[TestContext], None] = field(repr=False)
    known_risk: str = ""


def _check(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)

def tc01_register_new_user(ctx: TestContext) -> None:
    data = RegistrationData()
    ctx.register.register(data)
    _check(
        ctx.register.is_registered_successfully(),
        f"Registration of '{data.username}' did not show the success message. "
        f"Errors: {ctx.register.error_messages()}",
    )


def tc02_login_valid_credentials(ctx: TestContext) -> None:
    data = ctx.register_new_user()
    ctx.login.logout()
    ctx.login.open_login()
    ctx.login.login(data.username, data.password)
    _check(
        ctx.login.is_logged_in(),
        f"Login with valid credentials failed. Error: '{ctx.login.error_message()}'",
    )


def tc03_open_savings_account(ctx: TestContext) -> None:
    ctx.register_new_user()
    ctx.open_account.open_page()
    ctx.open_account.open_new_account(OpenAccountPage.SAVINGS)
    _check(ctx.open_account.is_account_opened(), "'Account Opened!' was not shown.")
    _check(
        bool(ctx.open_account.new_account_id()),
        "New account number was not displayed.",
    )


def tc04_transfer_between_accounts(ctx: TestContext) -> None:
    ctx.register_new_user()
    ctx.open_account.open_page()
    ctx.open_account.open_new_account(OpenAccountPage.SAVINGS)
    new_account = ctx.open_account.new_account_id()
    _check(bool(new_account), "Precondition failed: second account not created.")

    ctx.transfer.open_page()
    ctx.transfer.transfer("50", to_account=new_account)
    _check(
        ctx.transfer.is_transfer_complete(),
        f"Transfer was not completed. Error: '{ctx.transfer.error_message()}'",
    )


def tc05_update_contact_info(ctx: TestContext) -> None:
    ctx.register_new_user()
    ctx.profile.open_page()
    ctx.profile.update_contact_info(city="Novi Sad", phone="0611112222")
    _check(
        ctx.profile.is_profile_updated(),
        f"Profile update was not confirmed. Errors: {ctx.profile.error_messages()}",
    )


def tc06_login_wrong_password(ctx: TestContext) -> None:
    ctx.login.open_login()
    ctx.login.login("no_such_user_123", "wrong_password")
    error = ctx.login.error_message()
    _check(not ctx.login.is_logged_in(), "User was logged in with invalid data.")
    _check(
        "could not be verified" in error.lower(),
        f"Expected a 'could not be verified' error, got: '{error}'",
    )


def tc07_login_empty_fields(ctx: TestContext) -> None:
    ctx.login.open_login()
    ctx.login.login("", "")
    error = ctx.login.error_message()
    _check(not ctx.login.is_logged_in(), "User was logged in with empty fields.")
    _check(
        "enter a username and password" in error.lower(),
        f"Expected a 'enter a username and password' error, got: '{error}'",
    )


def tc08_register_password_mismatch(ctx: TestContext) -> None:
    data = RegistrationData(confirm_password="Different1!")
    ctx.register.register(data)
    _check(
        not ctx.register.is_registered_successfully(),
        "Registration succeeded although the passwords do not match.",
    )
    _check(
        ctx.register.has_error_containing("did not match"),
        f"Expected a 'did not match' error, got: {ctx.register.error_messages()}",
    )


def tc09_transfer_negative_amount(ctx: TestContext) -> None:
    ctx.register_new_user()
    ctx.open_account.open_page()
    ctx.open_account.open_new_account(OpenAccountPage.SAVINGS)
    new_account = ctx.open_account.new_account_id()
    _check(bool(new_account), "Precondition failed: second account not created.")

    ctx.transfer.open_page()
    ctx.transfer.transfer("-100", to_account=new_account)
    _check(
        not ctx.transfer.is_transfer_complete(),
        "DEFECT: the application accepted a transfer of a NEGATIVE amount (-100).",
    )


def tc10_transfer_non_numeric_amount(ctx: TestContext) -> None:
    ctx.register_new_user()
    ctx.transfer.open_page()
    ctx.transfer.transfer("abc")
    _check(
        not ctx.transfer.is_transfer_complete(),
        "Transfer was completed with a non-numeric amount ('abc').",
    )
    _check(
        bool(ctx.transfer.error_message()),
        "No error message was shown for a non-numeric amount.",
    )


def build_test_cases() -> list[TestCase]:
    return [
        TestCase(
            case_id="TC-01",
            title="Register a new user",
            test_type=TestType.POSITIVE,
            preconditions="Application is reachable. No user is logged in.",
            steps=[
                "Open the registration page.",
                "Fill in all fields with valid data and a unique username.",
                "Click 'Register'.",
            ],
            expected_result="The message 'Your account was created successfully' is shown.",
            execute=tc01_register_new_user,
        ),
        TestCase(
            case_id="TC-02",
            title="Login with valid credentials",
            test_type=TestType.POSITIVE,
            preconditions="A newly registered user exists.",
            steps=[
                "Register a new user and log out.",
                "Open the home page.",
                "Enter the valid username and password.",
                "Click 'Log In'.",
            ],
            expected_result="The 'Accounts Overview' page is displayed.",
            execute=tc02_login_valid_credentials,
        ),
        TestCase(
            case_id="TC-03",
            title="Open a new savings account",
            test_type=TestType.POSITIVE,
            preconditions="User is registered and logged in.",
            steps=[
                "Open the 'Open New Account' page.",
                "Select account type 'SAVINGS'.",
                "Click 'Open New Account'.",
            ],
            expected_result="'Account Opened!' is shown together with a new account number.",
            execute=tc03_open_savings_account,
        ),
        TestCase(
            case_id="TC-04",
            title="Transfer funds between own accounts",
            test_type=TestType.POSITIVE,
            preconditions="User is logged in and has two accounts.",
            steps=[
                "Open a second (savings) account.",
                "Open the 'Transfer Funds' page.",
                "Enter amount 50 and select the new account as the target.",
                "Click 'Transfer'.",
            ],
            expected_result="'Transfer Complete!' is shown.",
            execute=tc04_transfer_between_accounts,
        ),
        TestCase(
            case_id="TC-05",
            title="Update contact information",
            test_type=TestType.POSITIVE,
            preconditions="User is registered and logged in.",
            steps=[
                "Open the 'Update Contact Info' page.",
                "Change the city to 'Novi Sad' and the phone number.",
                "Click 'Update Profile'.",
            ],
            expected_result="'Profile Updated' confirmation is shown.",
            execute=tc05_update_contact_info,
        ),
        TestCase(
            case_id="TC-06",
            title="Login with a wrong password",
            test_type=TestType.NEGATIVE,
            preconditions="No user is logged in.",
            steps=[
                "Open the home page.",
                "Enter a non-existing username and a wrong password.",
                "Click 'Log In'.",
            ],
            expected_result="User is not logged in; an error says the credentials could not be verified.",
            execute=tc06_login_wrong_password,
        ),
        TestCase(
            case_id="TC-07",
            title="Login with empty fields",
            test_type=TestType.NEGATIVE,
            preconditions="No user is logged in.",
            steps=[
                "Open the home page.",
                "Leave username and password empty.",
                "Click 'Log In'.",
            ],
            expected_result="User is not logged in; an error asks for username and password.",
            execute=tc07_login_empty_fields,
        ),
        TestCase(
            case_id="TC-08",
            title="Register with mismatched passwords",
            test_type=TestType.NEGATIVE,
            preconditions="No user is logged in.",
            steps=[
                "Open the registration page.",
                "Fill in valid data, but use a different value in 'Confirm password'.",
                "Click 'Register'.",
            ],
            expected_result="Registration is rejected with a 'Passwords did not match' error.",
            execute=tc08_register_password_mismatch,
        ),
        TestCase(
            case_id="TC-09",
            title="Transfer a negative amount",
            test_type=TestType.NEGATIVE,
            preconditions="User is logged in and has two accounts.",
            steps=[
                "Open a second (savings) account.",
                "Open the 'Transfer Funds' page.",
                "Enter amount -100 and select the new account as the target.",
                "Click 'Transfer'.",
            ],
            expected_result="The transfer is rejected; 'Transfer Complete!' is NOT shown.",
            execute=tc09_transfer_negative_amount,
            known_risk="ParaBank is a demo app with weak validation; it may accept negative amounts (potential defect).",
        ),
        TestCase(
            case_id="TC-10",
            title="Transfer a non-numeric amount",
            test_type=TestType.NEGATIVE,
            preconditions="User is registered and logged in.",
            steps=[
                "Open the 'Transfer Funds' page.",
                "Enter the text 'abc' as the amount.",
                "Click 'Transfer'.",
            ],
            expected_result="The transfer is rejected and an error message is displayed.",
            execute=tc10_transfer_non_numeric_amount,
        ),
    ]