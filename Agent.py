from __future__ import annotations

import webbrowser

from ai.ai_assistant import AIAssistant
from config.settings import Settings
from core.browser_manager import BrowserManager
from core.test_runner import CaseResult, RunStatus, TestRunner
from reporting.report_writer import ReportWriter
from tests.test_cases import build_test_cases


class Agent:

    def __init__(self, settings: Settings | None = None) -> None:
        self._settings = settings or Settings()
        self._ai = AIAssistant(self._settings)
        self._reporter = ReportWriter(self._settings)

    def run(self) -> int:

        self._settings.ensure_directories()
        cases = build_test_cases()

        self._print_header(len(cases))


        cases_path = self._reporter.write_test_cases(cases)
        print(f"Test cases written to: {cases_path}\n")


        with BrowserManager(self._settings) as browser_manager:
            runner = TestRunner(self._settings, browser_manager)
            results = runner.run_all(cases)


        ai_summary = ""
        if self._ai.is_available:
            print("\nRunning AI analysis ...")
            self._ai.analyze_all(results)
            ai_summary = self._ai.summarize_run(results)
        else:
            print("\nAI analysis skipped (OPENROUTER_API_KEY is not set).")


        report_path = self._reporter.write_report(results, ai_summary)
        html_path = self._reporter.write_html_report(results, ai_summary)
        self._print_summary(results, str(report_path), str(html_path))
        webbrowser.open(html_path.as_uri())

        return 0 if all(r.status is RunStatus.PASSED for r in results) else 1


    def _print_header(self, total: int) -> None:
        print("=" * 60)
        print("ParaBank AI QA Agent")
        print(f"Application : {self._settings.base_url}")
        print(f"Test cases  : {total}")
        print(f"AI          : {'enabled' if self._ai.is_available else 'disabled'}")
        print("=" * 60 + "\n")

    @staticmethod
    def _print_summary(results: list[CaseResult], report_md: str, report_html: str) -> None:
        passed = sum(r.status is RunStatus.PASSED for r in results)
        failed = sum(r.status is RunStatus.FAILED for r in results)
        errors = sum(r.status is RunStatus.ERROR for r in results)
        print("\n" + "=" * 60)
        print(f"Passed: {passed}   Failed: {failed}   Errors: {errors}   Total: {len(results)}")
        print(f"Report (HTML): {report_html}")
        print(f"Report (MD)  : {report_md}")
        print("=" * 60)


if __name__ == "__main__":
    raise SystemExit(Agent().run())