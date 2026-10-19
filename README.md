# ParaBank AI QA Agent

**Automated UI testing with Python, Playwright, and AI-assisted failure analysis.**

ParaBank AI QA Agent is a QA automation project built to validate the core workflows of the [ParaBank demo banking application](https://parabank.parasoft.com/parabank). It combines browser-based functional testing, the **Page Object Model (POM)**, structured reporting, and optional analysis of failed tests using **OpenRouter AI**.

The project focuses on two complementary activities: **reliable, assertion-driven testing** and **faster investigation of unexpected results**. Every test executes a defined scenario and checks its expected outcome in code. AI can provide additional context when a test fails, but it does **not** decide the test result.

## Highlights

- **10 automated scenarios** covering essential banking workflows and invalid inputs
- **Positive and negative tests** with explicit expected outcomes
- **Playwright browser automation** organized using the **Page Object Model**
- **Programmatic assertions** for deterministic pass/fail decisions
- **HTML and Markdown reports** with test durations, errors, and screenshots
- **AI-assisted failure investigation** and an optional execution summary via OpenRouter
- **Single-command execution** through `Agent.py`, including direct execution from PyCharm

## Test coverage

The suite covers registration, authentication, account management, funds transfers, profile changes, and input validation.

| Test ID | Scenario | Type |
| :-- | :-- | :-- |
| TC-01 | Register a new user | Positive |
| TC-02 | Log in with valid credentials | Positive |
| TC-03 | Open a new savings account | Positive |
| TC-04 | Transfer funds between owned accounts | Positive |
| TC-05 | Update contact information | Positive |
| TC-06 | Attempt login with an incorrect password | Negative |
| TC-07 | Attempt login with empty fields | Negative |
| TC-08 | Register with mismatched passwords | Negative |
| TC-09 | Attempt to transfer a negative amount | Negative |
| TC-10 | Attempt to transfer a non-numeric amount | Negative |

Detailed test case documentation, including preconditions, test steps, and expected results, is generated in `artifacts/TEST_CASES.md`.

## Example test execution

The following results are from a sample run, **not a live or continuously updated test status**.

| ID | Test case | Result | Duration |
| :-- | :-- | :-- | --: |
| TC-01 | Register a new user | ✅ Passed | 10.5 s |
| TC-02 | Login with valid credentials | ✅ Passed | 10.9 s |
| TC-03 | Open a new savings account | ✅ Passed | 6.3 s |
| TC-04 | Transfer funds between own accounts | ✅ Passed | 10.8 s |
| TC-05 | Update contact information | ✅ Passed | 9.6 s |
| TC-06 | Login with a wrong password | ✅ Passed | 7.9 s |
| TC-07 | Login with empty fields | ✅ Passed | 7.9 s |
| TC-08 | Register with mismatched passwords | ✅ Passed | 10.3 s |
| TC-09 | Transfer a negative amount | ❌ Failed | 7.9 s |
| TC-10 | Transfer a non-numeric amount | ❌ Failed | 14.5 s |

**Sample summary: 10 executed · 8 passed · 2 failed · 80% pass rate · 96.5 s total**

### Findings from the sample run

- **TC-09:** ParaBank appeared to accept a transfer with a negative amount (`-100`), contrary to the test's expected validation behavior.
- **TC-10:** The application did not display the expected validation error for a non-numeric transfer amount.

These failed assertions highlight **potential application validation defects**. They should be reproduced and investigated before being classified as confirmed product bugs; they do not, by themselves, prove a defect in either the application or the test implementation.

<!-- Uncomment this line if docs/report.png exists in the repository: -->
<!-- ![Example HTML test report](docs/report.png) -->

## AI-assisted analysis

When a test fails, the framework can send the relevant failure details to a model through the **OpenRouter API**. The AI output supports investigation by:

1. Explaining plausible causes of the observed failure.
2. Suggesting whether the issue is more likely related to **application behavior**, **test implementation**, or the **execution environment**.
3. Recommending concrete next steps to reproduce or diagnose the issue.
4. Producing a concise summary of the overall execution.

> **AI is advisory, not authoritative.** A test passes or fails solely according to its programmed assertions. AI-generated classifications are hypotheses that must be verified.

**OpenRouter is optional:** all functional tests can run without an API key.

## Technology stack

| Technology / technique | Purpose |
| :-- | :-- |
| **Python** | Test logic, orchestration, and reporting |
| **Playwright** | Browser automation and UI interactions |
| **Page Object Model (POM)** | Reusable page-specific actions and locators |
| **Python assertions** | Deterministic result verification |
| **OpenRouter API** | Optional AI-assisted failure analysis |
| **HTML / Markdown** | Human-readable test documentation and reports |
| **Screenshots** | Visual evidence of test outcomes |
| **Environment variables** | Configuration of optional API credentials |

## Project structure

```text
ParaBank-AI-QA/
├── Agent.py                       # Main entry point for test execution
├── config/
│   └── settings.py                # URL, browser, AI model, output paths
├── core/
│   ├── browser_manager.py         # Browser lifecycle and session handling
│   └── test_runner.py             # Runs tests and captures evidence
├── pages/                         # Page Object Model classes
│   ├── base_page.py
│   ├── login_page.py
│   ├── register_page.py
│   ├── open_account_page.py
│   ├── transfer_funds_page.py
│   └── update_profile_page.py
├── tests/
│   └── test_cases.py              # TestCase definitions and 10 scenarios
├── ai/
│   └── ai_assistant.py            # OpenRouter integration and AI analysis
├── reporting/
│   └── report_writer.py           # Test case and result report generation
└── artifacts/                     # Generated during execution
    ├── TEST_CASES.md
    ├── TEST_REPORT.md
    ├── TEST_REPORT.html
    └── screenshots/
```

**Note:** The `artifacts/` directory represents generated output. An optional local `.env` file is not committed. If you add a report image, place it in `docs/report.png` and enable the image link above.

## Getting started

### 1. Clone the repository

```bash
git clone https://github.com/predragrujic/ParaBank-AI-QA.git
cd ParaBank-AI-QA
```

### 2. Install Python dependencies

Use an isolated virtual environment (recommended):

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\Activate.ps1
```

Or on macOS / Linux:

```bash
source .venv/bin/activate
```

Install the project's dependencies:

```bash
pip install -r requirements.txt
```

> **Repository check:** Ensure that `requirements.txt` has been committed before publishing these instructions. Without it, the installation command will not work.

### 3. Install Playwright's Chromium browser

```bash
playwright install chromium
```

### 4. Optional: configure OpenRouter

To enable AI analysis, create a `.env` file in the project root:

```dotenv
OPENROUTER_API_KEY=your_api_key_here
```

Keep the API key private, and ensure `.env` is excluded from Git. You can skip this step to run the tests without AI analysis.

## Running the tests

Start the test agent from the project directory:

```bash
python Agent.py
```

You can also open the project in **PyCharm** and run `Agent.py` directly.

The runner executes the defined scenarios, records outcomes, captures screenshots, and generates execution reports. When an OpenRouter key is configured, it can additionally request AI-assisted failure analysis and a run summary.

## Generated reports

After execution, results are written to `artifacts/`:

| Output | Description |
| :-- | :-- |
| `TEST_CASES.md` | Test specifications: preconditions, steps, expected results |
| `TEST_REPORT.md` | Detailed outcomes and captured evidence |
| `TEST_REPORT.html` | Standalone visual execution report with embedded screenshots |
| `screenshots/` | Screenshot captured after each test |

The HTML report can be opened locally in a browser to inspect the run without additional reporting tools.

## Design principles

**Assertion-first QA.** Expected results are defined explicitly in the tests. AI suggestions never override the actual pass/fail outcome.

**Maintainable page objects.** Page-specific locators and UI actions are grouped into dedicated classes instead of repeated throughout test cases.

**Scenario independence.** Tests are designed to avoid relying on previous test outcomes and to create the user data they need. Session reset is used between tests; this is not the same as full browser-context isolation.

**Evidence-driven investigation.** Reports retain execution outcomes, error details, and screenshots so failures can be investigated and reproduced.

**Optional AI enhancement.** AI helps interpret failures, while the automation remains usable without an AI provider.

## Project purpose

This project demonstrates a practical **QA automation workflow**: designing test cases, automating browser interactions, checking expected results, collecting execution evidence, and using AI to assist with failure triage.

It is intended as a portfolio project showcasing **Python, Playwright, POM architecture, positive and negative testing, test reporting, and responsible use of AI in software testing**.
