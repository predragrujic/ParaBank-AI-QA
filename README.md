# ParaBank AI QA Agent

Automated tests for the [ParaBank](https://parabank.parasoft.com/parabank) demo
banking app, built with Python, Playwright and the Page Object pattern.
When a test fails, an AI model (via OpenRouter) explains the likely cause.

Pass or fail is always decided by assertions, never by the AI.

## What is tested

10 test cases covering registration, login, opening an account, transferring
funds and updating a profile, including invalid input such as empty login
fields, mismatched passwords and invalid transfer amounts.
Full list: [artifacts/TEST_CASES.md](artifacts/TEST_CASES.md)

## Sample report

![Test execution report](docs/report.png)

## Project structure

```
parabank_ai_qa/
├── Agent.py                  # Single entry point (PyCharm Run button)
├── .env                      # OPENROUTER_API_KEY
├── requirements.txt
├── config/
│   └── settings.py           # Settings dataclass (URL, model, headless, paths)
├── ai/
│   └── ai_assistant.py       # AIAssistant: wraps OpenRouter (failure analysis, test data)
├── core/
│   ├── browser_manager.py    # One browser, one context, one page; always closed in finally
│   └── test_runner.py        # TestRunner: executes cases, screenshots on failure
├── pages/                    # Page Object Model
│   ├── base_page.py
│   ├── login_page.py
│   ├── register_page.py
│   ├── open_account_page.py
│   ├── transfer_funds_page.py
│   └── update_profile_page.py
├── tests/
│   └── test_cases.py         # TestCase dataclass + 10 test definitions
├── reporting/
│   └── report_writer.py      # Writes TEST_CASES.md and TEST_REPORT.md
└── artifacts/screenshots/
```


## Setup

​```
pip install -r requirements.txt
playwright install chromium
​```

Create a `.env` file in the project root:

​```
OPENROUTER_API_KEY=your_key_here
​```

The AI analysis is optional. Without a key the tests still run.

## Run

​```
python Agent.py
​```

Reports are written to the `artifacts/` folder.
