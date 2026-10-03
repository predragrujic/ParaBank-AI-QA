# ParaBank - Test Execution Report

- **Date:** 2026-10-03 14:03
- **Application:** https://parabank.parasoft.com/parabank
- **AI model:** ~openai/gpt-latest

## Summary

| Total | Passed | Failed | Errors | Pass rate | Duration |
|---|---|---|---|---|---|
| 10 | 8 | 2 | 0 | 80% | 96.5s |

## Executive summary (AI-generated)

> The automated test run achieved an 80% pass rate, with 8 of 10 tests passing. All positive scenarios passed, while two negative transfer-validation tests failed. The most important finding is that the application accepted a negative transfer amount of -100; non-numeric input also failed to produce an error message. Prioritize fixing transfer-amount validation to reject negative and non-numeric values with clear error messages, then rerun the affected tests.

## Results

| ID | Title | Type | Status | Duration |
|---|---|---|---|---|
| TC-01 | Register a new user | Positive | ✅ PASSED | 10.5s |
| TC-02 | Login with valid credentials | Positive | ✅ PASSED | 10.9s |
| TC-03 | Open a new savings account | Positive | ✅ PASSED | 6.3s |
| TC-04 | Transfer funds between own accounts | Positive | ✅ PASSED | 10.8s |
| TC-05 | Update contact information | Positive | ✅ PASSED | 9.6s |
| TC-06 | Login with a wrong password | Negative | ✅ PASSED | 7.9s |
| TC-07 | Login with empty fields | Negative | ✅ PASSED | 7.9s |
| TC-08 | Register with mismatched passwords | Negative | ✅ PASSED | 10.3s |
| TC-09 | Transfer a negative amount | Negative | ❌ FAILED | 7.9s |
| TC-10 | Transfer a non-numeric amount | Negative | ❌ FAILED | 14.5s |

## Test details

_FAILED = an assertion did not hold (possible application defect). ERROR = unexpected problem (timeout, missing element)._

### TC-01 - Register a new user ✅ PASSED

- **Type:** Positive
- **Duration:** 10.5s
- **Preconditions:** Application is reachable. No user is logged in.
- **Steps:**
  1. Open the registration page.
  2. Fill in all fields with valid data and a unique username.
  3. Click 'Register'.
- **Expected result:** The message 'Your account was created successfully' is shown.
- **Actual result:** Matches the expected result.
- **Final page URL:** https://parabank.parasoft.com/parabank/register.htm

![TC-01 screenshot](screenshots/TC-01_passed.png)

### TC-02 - Login with valid credentials ✅ PASSED

- **Type:** Positive
- **Duration:** 10.9s
- **Preconditions:** A newly registered user exists.
- **Steps:**
  1. Register a new user and log out.
  2. Open the home page.
  3. Enter the valid username and password.
  4. Click 'Log In'.
- **Expected result:** The 'Accounts Overview' page is displayed.
- **Actual result:** Matches the expected result.
- **Final page URL:** https://parabank.parasoft.com/parabank/overview.htm

![TC-02 screenshot](screenshots/TC-02_passed.png)

### TC-03 - Open a new savings account ✅ PASSED

- **Type:** Positive
- **Duration:** 6.3s
- **Preconditions:** User is registered and logged in.
- **Steps:**
  1. Open the 'Open New Account' page.
  2. Select account type 'SAVINGS'.
  3. Click 'Open New Account'.
- **Expected result:** 'Account Opened!' is shown together with a new account number.
- **Actual result:** Matches the expected result.
- **Final page URL:** https://parabank.parasoft.com/parabank/openaccount.htm

![TC-03 screenshot](screenshots/TC-03_passed.png)

### TC-04 - Transfer funds between own accounts ✅ PASSED

- **Type:** Positive
- **Duration:** 10.8s
- **Preconditions:** User is logged in and has two accounts.
- **Steps:**
  1. Open a second (savings) account.
  2. Open the 'Transfer Funds' page.
  3. Enter amount 50 and select the new account as the target.
  4. Click 'Transfer'.
- **Expected result:** 'Transfer Complete!' is shown.
- **Actual result:** Matches the expected result.
- **Final page URL:** https://parabank.parasoft.com/parabank/transfer.htm

![TC-04 screenshot](screenshots/TC-04_passed.png)

### TC-05 - Update contact information ✅ PASSED

- **Type:** Positive
- **Duration:** 9.6s
- **Preconditions:** User is registered and logged in.
- **Steps:**
  1. Open the 'Update Contact Info' page.
  2. Change the city to 'Novi Sad' and the phone number.
  3. Click 'Update Profile'.
- **Expected result:** 'Profile Updated' confirmation is shown.
- **Actual result:** Matches the expected result.
- **Final page URL:** https://parabank.parasoft.com/parabank/updateprofile.htm

![TC-05 screenshot](screenshots/TC-05_passed.png)

### TC-06 - Login with a wrong password ✅ PASSED

- **Type:** Negative
- **Duration:** 7.9s
- **Preconditions:** No user is logged in.
- **Steps:**
  1. Open the home page.
  2. Enter a non-existing username and a wrong password.
  3. Click 'Log In'.
- **Expected result:** User is not logged in; an error says the credentials could not be verified.
- **Actual result:** Matches the expected result.
- **Final page URL:** https://parabank.parasoft.com/parabank/login.htm

![TC-06 screenshot](screenshots/TC-06_passed.png)

### TC-07 - Login with empty fields ✅ PASSED

- **Type:** Negative
- **Duration:** 7.9s
- **Preconditions:** No user is logged in.
- **Steps:**
  1. Open the home page.
  2. Leave username and password empty.
  3. Click 'Log In'.
- **Expected result:** User is not logged in; an error asks for username and password.
- **Actual result:** Matches the expected result.
- **Final page URL:** https://parabank.parasoft.com/parabank/login.htm

![TC-07 screenshot](screenshots/TC-07_passed.png)

### TC-08 - Register with mismatched passwords ✅ PASSED

- **Type:** Negative
- **Duration:** 10.3s
- **Preconditions:** No user is logged in.
- **Steps:**
  1. Open the registration page.
  2. Fill in valid data, but use a different value in 'Confirm password'.
  3. Click 'Register'.
- **Expected result:** Registration is rejected with a 'Passwords did not match' error.
- **Actual result:** Matches the expected result.
- **Final page URL:** https://parabank.parasoft.com/parabank/register.htm

![TC-08 screenshot](screenshots/TC-08_passed.png)

### TC-09 - Transfer a negative amount ❌ FAILED

- **Type:** Negative
- **Duration:** 7.9s
- **Preconditions:** User is logged in and has two accounts.
- **Steps:**
  1. Open a second (savings) account.
  2. Open the 'Transfer Funds' page.
  3. Enter amount -100 and select the new account as the target.
  4. Click 'Transfer'.
- **Expected result:** The transfer is rejected; 'Transfer Complete!' is NOT shown.
- **Actual result:** DEFECT: the application accepted a transfer of a NEGATIVE amount (-100).
- **Final page URL:** https://parabank.parasoft.com/parabank/transfer.htm
- **Known risk:** ParaBank is a demo app with weak validation; it may accept negative amounts (potential defect).

![TC-09 screenshot](screenshots/TC-09_failed.png)

**AI analysis:**

> Likely cause: Missing positive-amount validation allowed the -100 transfer and displayed 'Transfer Complete!'.
> Category: Application defect
> Severity: High
> Suggested next step: Verify both account balances, enforce server-side rejection of non-positive amounts, and rerun TC-09.

### TC-10 - Transfer a non-numeric amount ❌ FAILED

- **Type:** Negative
- **Duration:** 14.5s
- **Preconditions:** User is registered and logged in.
- **Steps:**
  1. Open the 'Transfer Funds' page.
  2. Enter the text 'abc' as the amount.
  3. Click 'Transfer'.
- **Expected result:** The transfer is rejected and an error message is displayed.
- **Actual result:** No error message was shown for a non-numeric amount.
- **Final page URL:** https://parabank.parasoft.com/parabank/transfer.htm

![TC-10 screenshot](screenshots/TC-10_failed.png)

**AI analysis:**

> Likely cause: Non-numeric input triggered a generic internal error instead of the expected validation message, failing the assertion.
> Category: Application defect
> Severity: Medium
> Suggested next step: Reproduce with 'abc', inspect server logs, and verify the assertion targets the intended validation message.

