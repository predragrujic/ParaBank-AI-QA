# ParaBank - Test Cases

Application under test: https://parabank.parasoft.com/parabank

Total test cases: **10** (5 positive, 5 negative)

## Overview

| ID | Title | Type |
|---|---|---|
| TC-01 | Register a new user | Positive |
| TC-02 | Login with valid credentials | Positive |
| TC-03 | Open a new savings account | Positive |
| TC-04 | Transfer funds between own accounts | Positive |
| TC-05 | Update contact information | Positive |
| TC-06 | Login with a wrong password | Negative |
| TC-07 | Login with empty fields | Negative |
| TC-08 | Register with mismatched passwords | Negative |
| TC-09 | Transfer a negative amount | Negative |
| TC-10 | Transfer a non-numeric amount | Negative |

## Details

### TC-01 - Register a new user

- **Type:** Positive
- **Preconditions:** Application is reachable. No user is logged in.
- **Steps:**
  1. Open the registration page.
  2. Fill in all fields with valid data and a unique username.
  3. Click 'Register'.
- **Expected result:** The message 'Your account was created successfully' is shown.

### TC-02 - Login with valid credentials

- **Type:** Positive
- **Preconditions:** A newly registered user exists.
- **Steps:**
  1. Register a new user and log out.
  2. Open the home page.
  3. Enter the valid username and password.
  4. Click 'Log In'.
- **Expected result:** The 'Accounts Overview' page is displayed.

### TC-03 - Open a new savings account

- **Type:** Positive
- **Preconditions:** User is registered and logged in.
- **Steps:**
  1. Open the 'Open New Account' page.
  2. Select account type 'SAVINGS'.
  3. Click 'Open New Account'.
- **Expected result:** 'Account Opened!' is shown together with a new account number.

### TC-04 - Transfer funds between own accounts

- **Type:** Positive
- **Preconditions:** User is logged in and has two accounts.
- **Steps:**
  1. Open a second (savings) account.
  2. Open the 'Transfer Funds' page.
  3. Enter amount 50 and select the new account as the target.
  4. Click 'Transfer'.
- **Expected result:** 'Transfer Complete!' is shown.

### TC-05 - Update contact information

- **Type:** Positive
- **Preconditions:** User is registered and logged in.
- **Steps:**
  1. Open the 'Update Contact Info' page.
  2. Change the city to 'Novi Sad' and the phone number.
  3. Click 'Update Profile'.
- **Expected result:** 'Profile Updated' confirmation is shown.

### TC-06 - Login with a wrong password

- **Type:** Negative
- **Preconditions:** No user is logged in.
- **Steps:**
  1. Open the home page.
  2. Enter a non-existing username and a wrong password.
  3. Click 'Log In'.
- **Expected result:** User is not logged in; an error says the credentials could not be verified.

### TC-07 - Login with empty fields

- **Type:** Negative
- **Preconditions:** No user is logged in.
- **Steps:**
  1. Open the home page.
  2. Leave username and password empty.
  3. Click 'Log In'.
- **Expected result:** User is not logged in; an error asks for username and password.

### TC-08 - Register with mismatched passwords

- **Type:** Negative
- **Preconditions:** No user is logged in.
- **Steps:**
  1. Open the registration page.
  2. Fill in valid data, but use a different value in 'Confirm password'.
  3. Click 'Register'.
- **Expected result:** Registration is rejected with a 'Passwords did not match' error.

### TC-09 - Transfer a negative amount

- **Type:** Negative
- **Preconditions:** User is logged in and has two accounts.
- **Steps:**
  1. Open a second (savings) account.
  2. Open the 'Transfer Funds' page.
  3. Enter amount -100 and select the new account as the target.
  4. Click 'Transfer'.
- **Expected result:** The transfer is rejected; 'Transfer Complete!' is NOT shown.
- **Known risk:** ParaBank is a demo app with weak validation; it may accept negative amounts (potential defect).

### TC-10 - Transfer a non-numeric amount

- **Type:** Negative
- **Preconditions:** User is registered and logged in.
- **Steps:**
  1. Open the 'Transfer Funds' page.
  2. Enter the text 'abc' as the amount.
  3. Click 'Transfer'.
- **Expected result:** The transfer is rejected and an error message is displayed.

