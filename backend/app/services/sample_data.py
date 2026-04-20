from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[3]
SAMPLE_RESULT_PATH = ROOT / "demo" / "sample_json" / "sample_result.json"
SAMPLE_REPORT_PATH = ROOT / "demo" / "sample_outputs" / "sample_report.md"


def load_sample_result() -> dict:
    return json.loads(SAMPLE_RESULT_PATH.read_text(encoding="utf-8"))


def load_sample_report() -> str:
    return SAMPLE_REPORT_PATH.read_text(encoding="utf-8")


def build_sample_result(
    *,
    meeting_id: str,
    status: str = "completed",
    confidence: float | None = None,
    mode: str = "mock",
    reason: str = "Real pipeline not connected yet.",
    used_sample: bool = True,
) -> dict[str, Any]:
    payload = deepcopy(load_sample_result())
    payload["meeting_id"] = meeting_id
    payload["status"] = status
    if confidence is not None:
        payload["confidence"] = confidence
    payload["fallback"] = {
        **payload.get("fallback", {}),
        "mode": mode,
        "reason": reason,
        "used_sample": used_sample,
    }
    return payload
