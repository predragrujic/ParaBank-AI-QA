from __future__ import annotations

import time
from contextlib import suppress
from dataclasses import dataclass
from enum import Enum

from playwright.sync_api import Error as PlaywrightError

from config.settings import Settings
from core.browser_manager import BrowserManager
from tests.test_cases import TestCase, TestContext


class RunStatus(str, Enum):
    PASSED = "PASSED"
    FAILED = "FAILED"
    ERROR = "ERROR"


@dataclass
class CaseResult:
    case: TestCase
    status: RunStatus
    duration_s: float
    error_message: str = ""
    page_url: str = ""
    page_excerpt: str = ""
    screenshot_path: str = ""
    ai_analysis: str = ""


class TestRunner:
    __test__ = False

    EXCERPT_LENGTH = 800

    def __init__(self, settings: Settings, browser_manager: BrowserManager) -> None:
        self._settings = settings
        self._browser = browser_manager

    def run_all(self, cases: list[TestCase]) -> list[CaseResult]:
        results: list[CaseResult] = []
        total = len(cases)
        for index, case in enumerate(cases, start=1):
            print(f"[{index}/{total}] {case.case_id} - {case.title} ...", end=" ", flush=True)
            result = self.run_one(case)
            print(result.status.value)
            results.append(result)
        return results

    def run_one(self, case: TestCase) -> CaseResult:
        started = time.perf_counter()
        status = RunStatus.PASSED
        error_message = ""

        try:
            self._browser.reset_session()
            context = TestContext.create(self._browser.page, self._settings)
            case.execute(context)
        except AssertionError as exc:
            status = RunStatus.FAILED
            error_message = str(exc)
        except Exception as exc:  # noqa: BLE001 - runner must survive any error
            status = RunStatus.ERROR
            error_message = f"{type(exc).__name__}: {exc}"

        duration = time.perf_counter() - started
        result = CaseResult(
            case=case,
            status=status,
            duration_s=round(duration, 2),
            error_message=error_message,
        )

        self._capture_evidence(result)
        return result

    def _capture_evidence(self, result: CaseResult) -> None:
        with suppress(PlaywrightError, RuntimeError):
            result.page_url = self._browser.page.url

        if result.status is not RunStatus.PASSED:
            with suppress(PlaywrightError, RuntimeError):
                body_text = self._browser.page.locator("body").inner_text()
                result.page_excerpt = " ".join(body_text.split())[: self.EXCERPT_LENGTH]

        with suppress(PlaywrightError, RuntimeError, OSError):
            name = f"{result.case.case_id}_{result.status.value.lower()}"
            path = self._browser.take_screenshot(name)
            result.screenshot_path = str(path)