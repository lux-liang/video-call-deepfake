from __future__ import annotations

import copy
import hashlib
import json
import logging
import re
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
OUTPUTS_DIR = ROOT / "outputs"
SAMPLE_RESULT_PATH = ROOT / "demo" / "sample_json" / "sample_result.json"
VALIDATOR_VERSION = "phase1.pipeline.v1"
FIXED_BASE_TIME = datetime(2026, 4, 20, 0, 0, tzinfo=timezone.utc)

REQUIRED_TOP_LEVEL_FIELDS = (
    "meeting_id",
    "status",
    "confidence",
    "participants",
    "events",
    "responses",
    "risk_scores",
    "suspicious_segments",
    "tool_logs",
    "report_summary",
    "validation",
    "fallback",
)

REQUIRED_ITEM_FIELDS: dict[str, tuple[str, ...]] = {
    "participants": (
        "participant_id",
        "display_name",
        "role",
        "track_ref",
        "dominant_risk_level",
        "notes",
        "metadata",
    ),
    "events": (
        "event_id",
        "participant_id",
        "timestamp_start",
        "timestamp_end",
        "event_type",
        "severity",
        "summary",
        "evidence_refs",
    ),
    "responses": (
        "response_id",
        "kind",
        "source",
        "summary",
        "confidence",
    ),
    "risk_scores": (
        "participant_id",
        "score",
        "level",
        "reasons",
    ),
    "suspicious_segments": (
        "segment_id",
        "timestamp_start",
        "timestamp_end",
        "participant_ids",
        "reason",
        "confidence",
    ),
    "tool_logs": (
        "tool_name",
        "status",
        "started_at",
        "ended_at",
        "summary",
        "artifacts",
    ),
}

REQUIRED_OBJECT_FIELDS: dict[str, tuple[str, ...]] = {
    "report_summary": (
        "headline",
        "overview",
        "recommended_actions",
    ),
    "validation": (
        "schema_valid",
        "missing_fields",
        "warnings",
        "validator_version",
    ),
    "fallback": (
        "mode",
        "reason",
        "degraded_fields",
        "used_sample",
    ),
}


def configure_logging(name: str) -> logging.Logger:
    logging.basicConfig(
        level=logging.INFO,
        format="%(name)s %(levelname)s %(message)s",
    )
    return logging.getLogger(name)


def load_json(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def write_json(path: str | Path, payload: dict[str, Any]) -> Path:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return target


def emit_json(payload: dict[str, Any]) -> None:
    print(json.dumps(payload, ensure_ascii=False, indent=2))


def load_sample_result() -> dict[str, Any]:
    return load_json(SAMPLE_RESULT_PATH)


def stable_iso(offset_seconds: float = 0.0) -> str:
    instant = FIXED_BASE_TIME + timedelta(seconds=float(offset_seconds))
    return instant.strftime("%Y-%m-%dT%H:%M:%SZ")


def deterministic_int(key: str) -> int:
    return int(hashlib.sha256(key.encode("utf-8")).hexdigest()[:12], 16)


def deterministic_float(key: str, minimum: float, maximum: float, digits: int = 2) -> float:
    if minimum == maximum:
        return round(minimum, digits)
    span = maximum - minimum
    ratio = (deterministic_int(key) % 10_000) / 9_999
    return round(minimum + span * ratio, digits)


def sanitize_slug(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "_", value.lower()).strip("_")
    return slug or "meeting"


def default_meeting_id(video_path: str | None = None) -> str:
    if not video_path:
        return "meeting_demo_001"
    path = Path(video_path)
    stem = sanitize_slug(path.stem)[:24]
    suffix = hashlib.sha256(str(path).encode("utf-8")).hexdigest()[:6]
    return f"meeting_{stem}_{suffix}"


def build_tool_log(
    tool_name: str,
    status: str,
    summary: str,
    artifacts: list[str],
    start_offset: float,
    end_offset: float,
) -> dict[str, Any]:
    return {
        "tool_name": tool_name,
        "status": status,
        "started_at": stable_iso(start_offset),
        "ended_at": stable_iso(end_offset),
        "summary": summary,
        "artifacts": artifacts,
    }


def build_fallback(
    mode: str,
    reason: str,
    degraded_fields: list[str] | None = None,
    used_sample: bool = False,
) -> dict[str, Any]:
    return {
        "mode": mode,
        "reason": reason,
        "degraded_fields": list(degraded_fields or []),
        "used_sample": used_sample,
    }


def participant_templates() -> list[dict[str, Any]]:
    return [
        {
            "participant_id": "p_001",
            "display_name": "Alice",
            "role": "host",
            "track_ref": "video_track_1",
            "dominant_risk_level": "low",
            "notes": "No suspicious signal cluster recorded yet.",
            "metadata": {
                "seat_hint": "top-left",
                "speaker_label": "Speaker A",
            },
        },
        {
            "participant_id": "p_002",
            "display_name": "Bob",
            "role": "guest",
            "track_ref": "video_track_2",
            "dominant_risk_level": "low",
            "notes": "No suspicious signal cluster recorded yet.",
            "metadata": {
                "seat_hint": "top-right",
                "speaker_label": "Speaker B",
            },
        },
    ]


def participant_name_map(participants: list[dict[str, Any]]) -> dict[str, str]:
    return {item["participant_id"]: item["display_name"] for item in participants}


def derive_timeline(meeting_id: str, duration_seconds: float) -> dict[str, Any]:
    duration = max(90.0, float(duration_seconds))
    first_switch = round(max(8.0, duration * 0.10), 1)
    first_response_start = round(first_switch + 1.4, 1)
    first_response_end = round(first_response_start + 3.8, 1)
    screen_change_start = round(max(first_response_end + 24.0, duration * 0.47), 1)
    screen_change_end = round(min(duration - 18.0, screen_change_start + 2.5), 1)
    second_prompt_start = round(max(screen_change_end + 16.0, duration * 0.64), 1)
    second_response_start = round(second_prompt_start + 1.8, 1)
    second_response_end = round(min(duration - 1.0, second_response_start + 2.6), 1)

    speaker_turns = [
        {
            "turn_id": "turn_001",
            "participant_id": "p_002",
            "timestamp_start": 0.0,
            "timestamp_end": first_switch,
            "kind": "prompt",
            "addressed_participant_id": "p_001",
            "addressed_name": "Alice",
        },
        {
            "turn_id": "turn_002",
            "participant_id": "p_001",
            "timestamp_start": first_response_start,
            "timestamp_end": first_response_end,
            "kind": "named_response",
            "prompted_by_turn_id": "turn_001",
            "response_latency_seconds": round(first_response_start - first_switch, 1),
        },
        {
            "turn_id": "turn_003",
            "participant_id": "p_002",
            "timestamp_start": first_response_end + 8.0,
            "timestamp_end": second_prompt_start,
            "kind": "prompt",
            "addressed_participant_id": "p_001",
            "addressed_name": "Alice",
        },
        {
            "turn_id": "turn_004",
            "participant_id": "p_001",
            "timestamp_start": second_response_start,
            "timestamp_end": second_response_end,
            "kind": "named_response",
            "prompted_by_turn_id": "turn_003",
            "response_latency_seconds": round(second_response_start - second_prompt_start, 1),
        },
    ]

    screen_share_windows = [
        {
            "window_id": "screen_001",
            "timestamp_start": 0.0,
            "timestamp_end": screen_change_start,
            "state": "slides",
        },
        {
            "window_id": "screen_002",
            "timestamp_start": screen_change_start,
            "timestamp_end": screen_change_end,
            "state": "browser",
        },
        {
            "window_id": "screen_003",
            "timestamp_start": screen_change_end,
            "timestamp_end": duration,
            "state": "slides",
        },
    ]

    key_timestamps = [0.0, first_switch, first_response_start, first_response_end, screen_change_start, screen_change_end, second_response_start, second_response_end, duration]
    frames = []
    seen: set[float] = set()
    for timestamp in key_timestamps:
        rounded = round(timestamp, 1)
        if rounded in seen:
            continue
        seen.add(rounded)
        frames.append(
            {
                "frame_id": f"frame_{int(round(rounded * 30)):06d}",
                "timestamp": rounded,
                "artifact_ref": f"frame:{int(round(rounded * 30)):06d}",
            }
        )

    return {
        "meeting_id": meeting_id,
        "duration_seconds": round(duration, 1),
        "frames": frames,
        "speaker_turns": speaker_turns,
        "screen_share_windows": screen_share_windows,
    }


def result_for_meeting(meeting_id: str) -> dict[str, Any]:
    payload = copy.deepcopy(load_sample_result())
    if meeting_id == payload["meeting_id"]:
        return payload
    return replace_strings(payload, payload["meeting_id"], meeting_id)


def replace_strings(value: Any, source: str, target: str) -> Any:
    if isinstance(value, dict):
        return {key: replace_strings(item, source, target) for key, item in value.items()}
    if isinstance(value, list):
        return [replace_strings(item, source, target) for item in value]
    if isinstance(value, str):
        return value.replace(source, target)
    return value


def merge_unique(items: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for item in items:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result


def collect_missing_fields(payload: dict[str, Any]) -> list[str]:
    missing: list[str] = []

    for field in REQUIRED_TOP_LEVEL_FIELDS:
        if field not in payload:
            missing.append(field)

    for field, required_fields in REQUIRED_ITEM_FIELDS.items():
        value = payload.get(field)
        if not isinstance(value, list):
            missing.append(field)
            continue
        if field == "responses" and not value:
            missing.append("responses[0]")
        for index, item in enumerate(value):
            if not isinstance(item, dict):
                missing.append(f"{field}[{index}]")
                continue
            for required in required_fields:
                if required not in item:
                    missing.append(f"{field}[{index}].{required}")

    for field, required_fields in REQUIRED_OBJECT_FIELDS.items():
        value = payload.get(field)
        if not isinstance(value, dict):
            missing.append(field)
            continue
        for required in required_fields:
            if required not in value:
                missing.append(f"{field}.{required}")

    return missing


def build_validation(payload: dict[str, Any], warnings: list[str] | None = None) -> dict[str, Any]:
    merged_warnings = list(warnings or [])
    existing_validation = payload.get("validation")
    if isinstance(existing_validation, dict):
        merged_warnings.extend(str(item) for item in existing_validation.get("warnings", []))
    payload_for_validation = copy.deepcopy(payload)
    payload_for_validation["validation"] = {
        "schema_valid": True,
        "missing_fields": [],
        "warnings": [],
        "validator_version": VALIDATOR_VERSION,
    }
    missing_fields = collect_missing_fields(payload_for_validation)
    return {
        "schema_valid": not missing_fields,
        "missing_fields": missing_fields,
        "warnings": merge_unique(merged_warnings),
        "validator_version": VALIDATOR_VERSION,
    }


def level_from_score(score: float) -> str:
    if score >= 0.75:
        return "high"
    if score >= 0.45:
        return "medium"
    return "low"


def artifact_dir(meeting_id: str) -> Path:
    return OUTPUTS_DIR / meeting_id
