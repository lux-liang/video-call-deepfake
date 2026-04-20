from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
SAMPLE_RESULT_PATH = ROOT / "demo" / "sample_json" / "sample_result.json"
SAMPLE_REPORT_PATH = ROOT / "demo" / "sample_outputs" / "sample_report.md"


def load_sample_result() -> dict:
    return json.loads(SAMPLE_RESULT_PATH.read_text(encoding="utf-8"))


def load_sample_report() -> str:
    return SAMPLE_REPORT_PATH.read_text(encoding="utf-8")
