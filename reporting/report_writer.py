from __future__ import annotations

import base64
from datetime import datetime
from html import escape
from pathlib import Path

from config.settings import Settings
from core.test_runner import CaseResult, RunStatus
from tests.test_cases import TestCase

STATUS_ICONS = {
    RunStatus.PASSED: "✅",
    RunStatus.FAILED: "❌",
    RunStatus.ERROR: "⚠️",
}
STATUS_COLORS = {
    RunStatus.PASSED: "#1a7f37",
    RunStatus.FAILED: "#cf222e",
    RunStatus.ERROR: "#bf8700",
}

HTML_STYLE = """
body{font-family:Segoe UI,Arial,sans-serif;max-width:1000px;margin:30px auto;padding:0 16px;color:#1f2328;background:#f6f8fa}
h1{margin-bottom:4px} .meta{color:#656d76;font-size:14px}
.cards{display:flex;gap:12px;flex-wrap:wrap;margin:20px 0}
.card{background:#fff;border:1px solid #d0d7de;border-radius:8px;padding:12px 18px;min-width:110px}
.card span{display:block;font-size:12px;color:#656d76} .card strong{font-size:24px}
table{border-collapse:collapse;width:100%;background:#fff;margin-bottom:24px}
th,td{border:1px solid #d0d7de;padding:8px 10px;text-align:left;font-size:14px}
th{background:#eaeef2}
.badge{color:#fff;border-radius:12px;padding:2px 10px;font-size:12px;vertical-align:middle}
.case{background:#fff;border:1px solid #d0d7de;border-radius:8px;padding:8px 20px 16px;margin-bottom:20px}
.case img{max-width:100%;border:1px solid #d0d7de;border-radius:6px;margin-top:8px}
.ai{background:#f1f8ff;border-left:4px solid #0969da;padding:4px 14px;margin-top:12px}
.ai pre{white-space:pre-wrap;font-family:inherit;margin:6px 0}
blockquote{background:#fff;border-left:4px solid #0969da;margin:0 0 24px;padding:8px 16px}
a{color:#0969da;text-decoration:none}
"""


def _cell(text: str) -> str:
    return " ".join(str(text).split()).replace("|", "\\|")


class ReportWriter:
    def __init__(self, settings: Settings) -> None:
        self._settings = settings

    def write_test_cases(self, cases: list[TestCase]) -> Path:
        lines: list[str] = [
            "# ParaBank - Test Cases",
            "",
            f"Application under test: {self._settings.base_url}",
            "",
            f"Total test cases: **{len(cases)}** "
            f"({sum(c.test_type.value == 'Positive' for c in cases)} positive, "
            f"{sum(c.test_type.value == 'Negative' for c in cases)} negative)",
            "",
            "## Overview",
            "",
            "| ID | Title | Type |",
            "|---|---|---|",
        ]
        for case in cases:
            lines.append(
                f"| {case.case_id} | {_cell(case.title)} | {case.test_type.value} |"
            )

        lines += ["", "## Details", ""]
        for case in cases:
            lines += [
                f"### {case.case_id} - {case.title}",
                "",
                f"- **Type:** {case.test_type.value}",
                f"- **Preconditions:** {case.preconditions}",
                "- **Steps:**",
            ]
            lines += [f"  {i}. {step}" for i, step in enumerate(case.steps, start=1)]
            lines.append(f"- **Expected result:** {case.expected_result}")
            if case.known_risk:
                lines.append(f"- **Known risk:** {case.known_risk}")
            lines.append("")

        return self._write(self._settings.test_cases_md, lines)

    def write_report(self, results: list[CaseResult], ai_summary: str = "") -> Path:
        total, passed, failed, errors, duration = self._stats(results)
        pass_rate = (passed / total * 100) if total else 0.0

        lines: list[str] = [
            "# ParaBank - Test Execution Report",
            "",
            f"- **Date:** {datetime.now():%Y-%m-%d %H:%M}",
            f"- **Application:** {self._settings.base_url}",
            f"- **AI model:** {self._ai_label()}",
            "",
            "## Summary",
            "",
            "| Total | Passed | Failed | Errors | Pass rate | Duration |",
            "|---|---|---|---|---|---|",
            f"| {total} | {passed} | {failed} | {errors} | {pass_rate:.0f}% | {duration:.1f}s |",
            "",
        ]

        if ai_summary:
            lines += ["## Executive summary (AI-generated)", ""]
            lines += [f"> {line}" for line in ai_summary.splitlines() if line.strip()]
            lines.append("")

        lines += [
            "## Results",
            "",
            "| ID | Title | Type | Status | Duration |",
            "|---|---|---|---|---|",
        ]
        for r in results:
            lines.append(
                f"| {r.case.case_id} | {_cell(r.case.title)} | {r.case.test_type.value} "
                f"| {STATUS_ICONS[r.status]} {r.status.value} | {r.duration_s:.1f}s |"
            )

        lines += [
            "",
            "## Test details",
            "",
            "_FAILED = an assertion did not hold (possible application defect). "
            "ERROR = unexpected problem (timeout, missing element)._",
            "",
        ]
        for r in results:
            lines += self._md_case(r)

        return self._write(self._settings.test_report_md, lines)

    def write_html_report(self, results: list[CaseResult], ai_summary: str = "") -> Path:
        total, passed, failed, errors, duration = self._stats(results)
        pass_rate = (passed / total * 100) if total else 0.0

        cards = "".join(
            f"<div class='card'><span>{label}</span>"
            f"<strong style='color:{color}'>{value}</strong></div>"
            for label, value, color in [
                ("Total", total, "#1f2328"),
                ("Passed", passed, STATUS_COLORS[RunStatus.PASSED]),
                ("Failed", failed, STATUS_COLORS[RunStatus.FAILED]),
                ("Errors", errors, STATUS_COLORS[RunStatus.ERROR]),
                ("Pass rate", f"{pass_rate:.0f}%", "#1f2328"),
                ("Duration", f"{duration:.1f}s", "#1f2328"),
            ]
        )

        rows = "".join(
            f"<tr><td><a href='#{r.case.case_id.lower()}'>{escape(r.case.case_id)}</a></td>"
            f"<td>{escape(r.case.title)}</td><td>{r.case.test_type.value}</td>"
            f"<td><span class='badge' style='background:{STATUS_COLORS[r.status]}'>"
            f"{r.status.value}</span></td><td>{r.duration_s:.1f}s</td></tr>"
            for r in results
        )

        parts = [
            "<!DOCTYPE html><html lang='en'><head><meta charset='utf-8'>",
            "<title>ParaBank - Test Execution Report</title>",
            f"<style>{HTML_STYLE}</style></head><body>",
            "<h1>ParaBank - Test Execution Report</h1>",
            f"<p class='meta'>{datetime.now():%Y-%m-%d %H:%M} &middot; "
            f"{escape(self._settings.base_url)} &middot; AI model: {escape(self._ai_label())}</p>",
            f"<div class='cards'>{cards}</div>",
        ]
        if ai_summary:
            parts.append(
                "<h2>Executive summary (AI-generated)</h2>"
                f"<blockquote>{escape(ai_summary).replace(chr(10), '<br>')}</blockquote>"
            )
        parts.append(
            "<h2>Results</h2><table><tr><th>ID</th><th>Title</th><th>Type</th>"
            f"<th>Status</th><th>Duration</th></tr>{rows}</table>"
        )
        parts.append("<h2>Test details</h2>")
        parts += [self._html_case(r) for r in results]
        parts.append("</body></html>")

        path = self._settings.test_report_html
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("".join(parts), encoding="utf-8")
        return path

    def _md_case(self, result: CaseResult) -> list[str]:
        case = result.case
        lines = [
            f"### {case.case_id} - {case.title} {STATUS_ICONS[result.status]} {result.status.value}",
            "",
            f"- **Type:** {case.test_type.value}",
            f"- **Duration:** {result.duration_s:.1f}s",
            f"- **Preconditions:** {case.preconditions}",
            "- **Steps:**",
        ]
        lines += [f"  {i}. {step}" for i, step in enumerate(case.steps, start=1)]
        lines += [
            f"- **Expected result:** {case.expected_result}",
            f"- **Actual result:** {self._actual_result(result)}",
        ]
        if result.page_url:
            lines.append(f"- **Final page URL:** {result.page_url}")
        if case.known_risk:
            lines.append(f"- **Known risk:** {case.known_risk}")
        if result.screenshot_path:
            lines += [
                "",
                f"![{case.case_id} screenshot]({self._relative(result.screenshot_path)})",
            ]
        if result.ai_analysis:
            lines += ["", "**AI analysis:**", ""]
            lines += [f"> {line}" for line in result.ai_analysis.splitlines() if line.strip()]
        lines.append("")
        return lines

    def _html_case(self, result: CaseResult) -> str:
        case = result.case
        steps = "".join(f"<li>{escape(step)}</li>" for step in case.steps)
        parts = [
            f"<section class='case' id='{case.case_id.lower()}'>",
            f"<h3>{escape(case.case_id)} - {escape(case.title)} "
            f"<span class='badge' style='background:{STATUS_COLORS[result.status]}'>"
            f"{result.status.value}</span></h3>",
            f"<p class='meta'>{case.test_type.value} &middot; {result.duration_s:.1f}s</p>",
            f"<p><b>Preconditions:</b> {escape(case.preconditions)}</p>",
            f"<p><b>Steps:</b></p><ol>{steps}</ol>",
            f"<p><b>Expected result:</b> {escape(case.expected_result)}</p>",
            f"<p><b>Actual result:</b> {escape(self._actual_result(result))}</p>",
        ]
        if result.page_url:
            parts.append(f"<p><b>Final page URL:</b> {escape(result.page_url)}</p>")
        if case.known_risk:
            parts.append(f"<p><b>Known risk:</b> {escape(case.known_risk)}</p>")
        image = self._image_data_uri(result.screenshot_path)
        if image:
            parts.append(f"<img src='{image}' alt='{escape(case.case_id)} screenshot'>")
        if result.ai_analysis:
            parts.append(
                f"<div class='ai'><b>AI analysis</b><pre>{escape(result.ai_analysis)}</pre></div>"
            )
        parts.append("</section>")
        return "".join(parts)

    @staticmethod
    def _actual_result(result: CaseResult) -> str:
        if result.status is RunStatus.PASSED:
            return "Matches the expected result."
        return result.error_message or "-"

    @staticmethod
    def _stats(results: list[CaseResult]) -> tuple[int, int, int, int, float]:
        total = len(results)
        passed = sum(r.status is RunStatus.PASSED for r in results)
        failed = sum(r.status is RunStatus.FAILED for r in results)
        errors = sum(r.status is RunStatus.ERROR for r in results)
        duration = sum(r.duration_s for r in results)
        return total, passed, failed, errors, duration

    def _ai_label(self) -> str:
        return self._settings.ai_model if self._settings.ai_enabled else "disabled"

    def _relative(self, screenshot_path: str) -> str:
        try:
            return Path(screenshot_path).relative_to(self._settings.artifacts_dir).as_posix()
        except ValueError:
            return Path(screenshot_path).as_posix()

    @staticmethod
    def _image_data_uri(screenshot_path: str) -> str:
        if not screenshot_path:
            return ""
        try:
            data = base64.b64encode(Path(screenshot_path).read_bytes()).decode("ascii")
        except OSError:
            return ""
        return f"data:image/png;base64,{data}"

    @staticmethod
    def _write(path: Path, lines: list[str]) -> Path:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        return path