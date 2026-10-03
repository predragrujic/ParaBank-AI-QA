from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path

from dotenv import load_dotenv

PROJECT_ROOT: Path = Path(__file__).resolve().parent.parent

load_dotenv(PROJECT_ROOT / ".env")


@dataclass(frozen=True)
class Settings:
    base_url: str = "https://parabank.parasoft.com/parabank"

    headless: bool = False
    slow_mo_ms: int = 250
    default_timeout_ms: int = 15_000
    viewport_width: int = 1366
    viewport_height: int = 850

    openrouter_api_key: str = field(
        default_factory=lambda: os.getenv("OPENROUTER_API_KEY", "")
    )
    ai_model: str = "~openai/gpt-latest"
    ai_fallback_model: str = "openrouter/auto-beta"
    ai_max_tokens: int = 600

    artifacts_dir: Path = PROJECT_ROOT / "artifacts"
    screenshots_dir: Path = PROJECT_ROOT / "artifacts" / "screenshots"
    test_cases_md: Path = PROJECT_ROOT / "artifacts" / "TEST_CASES.md"
    test_report_md: Path = PROJECT_ROOT / "artifacts" / "TEST_REPORT.md"
    test_report_html: Path = PROJECT_ROOT / "artifacts" / "TEST_REPORT.html"

    @property
    def ai_enabled(self) -> bool:
        return bool(self.openrouter_api_key.strip())

    @property
    def home_url(self) -> str:
        return f"{self.base_url}/index.htm"

    def ensure_directories(self) -> None:
        self.screenshots_dir.mkdir(parents=True, exist_ok=True)