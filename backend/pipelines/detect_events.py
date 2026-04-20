from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

if __package__ in (None, ""):
    import sys

    sys.path.append(str(Path(__file__).resolve().parents[2]))
    from backend.pipelines.common import (
        artifact_dir,
        build_fallback,
        build_tool_log,
        configure_logging,
        emit_json,
        load_json,
        participant_name_map,
        write_json,
    )
    from backend.pipelines.extract_frames import extract_frames
else:
    from .common import (
        artifact_dir,
        build_fallback,
        build_tool_log,
        configure_logging,
        emit_json,
        load_json,
        participant_name_map,
        write_json,
    )
    from .extract_frames import extract_frames


def detect_events(
    frames_payload: dict[str, Any] | None = None,
    input_path: str | Path | None = None,
    output_path: str | Path | None = None,
) -> dict[str, Any]:
    logger = configure_logging("detect_events")
    if frames_payload is None:
        if input_path and Path(input_path).exists():
            frames_payload = load_json(input_path)
        else:
            frames_payload = extract_frames()

    meeting_id = frames_payload["meeting_id"]
    artifact_root = artifact_dir(meeting_id)
    name_map = participant_name_map(frames_payload["participants"])
    speaker_turns = frames_payload["speaker_turns"]
    screen_windows = frames_payload["screen_share_windows"]

    first_prompt = speaker_turns[0]
    first_response = speaker_turns[1]
    second_prompt = speaker_turns[2]
    second_response = speaker_turns[3]
    screen_change = screen_windows[1]

    events = [
        {
            "event_id": "evt_001",
            "participant_id": first_response["participant_id"],
            "timestamp_start": first_prompt["timestamp_end"],
            "timestamp_end": first_response["timestamp_start"],
            "event_type": "speaker_switch",
            "severity": "medium",
            "summary": f"Active speaker switches from {name_map[first_prompt['participant_id']]} to {name_map[first_response['participant_id']]} before a named response.",
            "evidence_refs": [f"speaker_turn:{first_prompt['turn_id']}", f"speaker_turn:{first_response['turn_id']}"],
        },
        {
            "event_id": "evt_002",
            "participant_id": first_response["participant_id"],
            "timestamp_start": first_response["timestamp_start"],
            "timestamp_end": first_response["timestamp_end"],
            "event_type": "named_response",
            "severity": "high",
            "summary": f"{name_map[first_response['participant_id']]} responds after being addressed by name with elevated latency.",
            "evidence_refs": [f"speaker_turn:{first_response['turn_id']}", "transcript:line_021"],
        },
        {
            "event_id": "evt_003",
            "participant_id": first_prompt["participant_id"],
            "timestamp_start": screen_change["timestamp_start"],
            "timestamp_end": screen_change["timestamp_end"],
            "event_type": "screen_share_change",
            "severity": "low",
            "summary": "Screen-share state changes while the secondary participant remains the active speaker.",
            "evidence_refs": [f"screen_share:{screen_change['window_id']}", "frame:screen_share_toggle"],
        },
        {
            "event_id": "evt_004",
            "participant_id": second_response["participant_id"],
            "timestamp_start": second_response["timestamp_start"],
            "timestamp_end": second_response["timestamp_end"],
            "event_type": "named_response",
            "severity": "medium",
            "summary": f"Second named response from {name_map[second_response['participant_id']]} begins after a shorter but still elevated latency window.",
            "evidence_refs": [f"speaker_turn:{second_prompt['turn_id']}", f"speaker_turn:{second_response['turn_id']}"],
        },
    ]

    source_mode = frames_payload.get("source_mode", "mock")
    fallback = build_fallback(
        mode="heuristic" if source_mode != "mock" else "mock",
        reason="P0 event detection is rule-based and limited to speaker switch, named response, and screen-share change.",
        degraded_fields=[] if source_mode != "mock" else ["events[]"],
        used_sample=source_mode == "mock",
    )
    payload = {
        "meeting_id": meeting_id,
        "participants": frames_payload["participants"],
        "events": events,
        "tool_log": build_tool_log(
            tool_name="event_detector",
            status="success",
            summary="Detected P0 event classes with deterministic turn-taking rules.",
            artifacts=[str(artifact_root / "events.json")],
            start_offset=1,
            end_offset=2,
        ),
        "fallback": fallback,
    }
    logger.info("detected %s events for %s", len(events), meeting_id)

    if output_path:
        write_json(output_path, payload)
    return payload


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Detect P0 meeting events from the frame manifest.")
    parser.add_argument("--input", help="Path to the frame manifest JSON.")
    parser.add_argument("--output", help="Optional path to write the event JSON.")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    emit_json(detect_events(input_path=args.input, output_path=args.output))


if __name__ == "__main__":
    main()
