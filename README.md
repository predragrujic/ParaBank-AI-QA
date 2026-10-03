# ParaBank AI QA Agent

An automated QA test agent for the [ParaBank](https://parabank.parasoft.com/parabank) demo banking application, built in Python with **Playwright**, the **Page Object Model (POM)** and **OpenRouter AI**.

The project combines classic UI automation with AI-assisted failure analysis. Tests execute predefined scenarios, verify the expected results with assertions and generate execution reports.

> **Important:** the AI never decides whether a test passed or failed. The test status is determined exclusively by programmatic assertions. The AI is used only to help analyze tests that did not pass and to summarize the run.

## What is tested

The project contains **10 independent test cases** covering the key functionality of ParaBank:

* User registration
* User login
* Opening a bank account
* Funds transfer
* Profile update
* Validation of invalid user input
* Empty login fields
* Mismatched passwords
* Invalid transfer amounts

The full specification of every test case (preconditions, steps, expected result) is generated into:

`artifacts/TEST_CASES.md`

## Sample report

![Test execution report](docs/report.png)

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

**Result of the sample run:** 10 tests, 8 passed, 2 failed (80% pass rate, 96.5s).

TC-09 and TC-10 failed because ParaBank accepted a transfer of a negative amount (-100) and did not show an error message for a non-numeric amount. These are findings about the application, not problems in the test code.

## AI analysis

When a test does not pass, the agent sends the error details to an AI model through **OpenRouter**.

The AI analysis helps with:

* identifying the likely cause of the failure
* classifying it as an application defect, a test script issue or an environment issue
* suggesting a next step for investigation
* writing a short executive summary of the whole run

The AI functionality is optional. **The tests run without an OpenRouter API key as well.**

## Technologies

* **Python**
* **Playwright**
* **OpenRouter API**
* **Page Object Model (POM)**
* **Plain Python assertions** (deterministic pass/fail)
* **Markdown and HTML reports**
* **Screenshot after every test**
* **Environment variables**

## Project structure

```text
parabank_ai_qa/
│
├── Agent.py                    # Single entry point (PyCharm Run button)
├── .env                        # OPENROUTER_API_KEY (not part of the repository)
├── requirements.txt
│
├── config/
│   └── settings.py             # Settings dataclass (URL, model, headless, paths)
│
├── ai/
│   └── ai_assistant.py         # AIAssistant: wraps OpenRouter (failure analysis, run summary)
│
├── core/
│   ├── browser_manager.py      # One browser, one context, one page; always closed
│   └── test_runner.py          # TestRunner: executes cases, screenshot after every test
│
├── pages/                      # Page Object Model
│   ├── base_page.py
│   ├── login_page.py
│   ├── register_page.py
│   ├── open_account_page.py
│   ├── transfer_funds_page.py
│   └── update_profile_page.py
│
├── tests/
│   └── test_cases.py           # TestCase dataclass + 10 test definitions
│
├── reporting/
│   └── report_writer.py        # Writes TEST_CASES.md, TEST_REPORT.md and TEST_REPORT.html
│
├── docs/
│   └── report.png              # Sample report screenshot used in this README
│
└── artifacts/
    ├── TEST_CASES.md
    ├── TEST_REPORT.md
    ├── TEST_REPORT.html
    └── screenshots/
```

## Setup

Clone the repository:

```bash
git clone https://github.com/predragrujic/ParaBank-AI-QA.git
cd ParaBank-AI-QA
```

Install the required Python packages:

```bash
pip install -r requirements.txt
```

Install Chromium for Playwright:

```bash
playwright install chromium
```

### OpenRouter API key

The AI analysis is optional.

To use it, create a `.env` file in the project root:

```env
OPENROUTER_API_KEY=your_key_here
```

The API key is never stored in the Git repository.

## Running the tests

The project is started through the main `Agent.py` file:

```bash
python Agent.py
```

In PyCharm you can run it directly with the **Run** button on `Agent.py`.

## Reports

After the run, the results are saved in the `artifacts/` folder.

The following files are generated:

* `TEST_CASES.md` - overview of all test cases
* `TEST_REPORT.md` - detailed result of every test, with screenshots
* `TEST_REPORT.html` - self-contained report with embedded screenshots, opened automatically in the browser after the run
* `screenshots/` - a screenshot taken after every test

## QA approach

The project is built around a few principles:

**Deterministic results**
The test status is determined by assertions and expected results, not by the AI model.

**Page Object Model**
UI interactions are separated from the test logic for better organization and maintainability.

**Independent tests**
Every test starts from a clean session and registers its own user, so test cases can be executed individually.

**Failure evidence**
A screenshot is saved after every test, and for failed tests the error message and page content are kept for further analysis.

**AI as a helper**
The AI is used for failure analysis and the run summary, but it does not replace the core test logic.

## Project goal

The goal of the project is to demonstrate the practical use of **UI test automation and AI tools in the QA process**, with a clear separation between deterministic testing and AI-assisted analysis.

The project is a portfolio example of work with:

* UI test automation
* Page Object Model architecture
* negative test scenarios
* validation of user input
* automated reporting
* screenshots as test evidence
* AI-assisted analysis of failed tests
