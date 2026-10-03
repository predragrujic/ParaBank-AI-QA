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

​```
Agent.py          # entry point, runs the whole flow
config/           # settings
core/             # browser manager, test runner
pages/            # page objects
tests/            # test case definitions
ai/               # OpenRouter assistant
reporting/        # Markdown and HTML reports
​```

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
