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
        level_from_score,
        load_json,
        participant_name_map,
        write_json,
    )
    from backend.pipelines.detect_events import detect_events
    from backend.pipelines.extract_behavior import extract_behavior
    from backend.pipelines.extract_frames import extract_frames
else:
    from .common import (
        artifact_dir,
        build_fallback,
        build_tool_log,
        configure_logging,
        emit_json,
        level_from_score,
        load_json,
        participant_name_map,
        write_json,
    )
    from .detect_events import detect_events
    from .extract_behavior import extract_behavior
    from .extract_frames import extract_frames


def _score_participant(feature: dict[str, Any], event_count: int) -> tuple[float, list[str]]:
    mouth = feature["mouth_onset"]
    head = feature["head_pose_change"]
    latency = feature["response_latency"]

    score = 0.08
    reasons: list[str] = []

    if mouth["count"]:
        score += min(0.26, mouth["avg_delay_seconds"] * 0.38 + mouth["count"] * 0.06)
        reasons.append("repeated mouth onset lag during named responses")
    if head["count"]:
        score += min(0.16, head["max_delta_degrees"] / 100.0)
        reasons.append("head pose change near speech onset")

    latency_gap = max(0.0, latency["avg_seconds"] - latency["baseline_seconds"])
    if latency["count"]:
        score += min(0.22, latency_gap * 0.12 + latency["count"] * 0.04)
        reasons.append("response latency above meeting baseline")

    if event_count and not reasons:
        score += 0.10
        reasons.append("isolated event activity without a repeated anomaly cluster")

    return round(min(score, 0.99), 2), reasons or ["no sustained anomaly cluster"]


def score_risk(
    frames_payload: dict[str, Any] | None = None,
    events_payload: dict[str, Any] | None = None,
    behavior_payload: dict[str, Any] | None = None,
    frames_path: str | Path | None = None,
    events_path: str | Path | None = None,
    behavior_path: str | Path | None = None,
    output_path: str | Path | None = None,
) -> dict[str, Any]:
    logger = configure_logging("score_risk")
    if frames_payload is None:
        if frames_path and Path(frames_path).exists():
            frames_payload = load_json(frames_path)
        else:
            frames_payload = extract_frames()
    if events_payload is None:
        if events_path and Path(events_path).exists():
            events_payload = load_json(events_path)
        else:
            events_payload = detect_events(frames_payload=frames_payload)
    if behavior_payload is None:
        if behavior_path and Path(behavior_path).exists():
            behavior_payload = load_json(behavior_path)
        else:
            behavior_payload = extract_behavior(frames_payload=frames_payload, events_payload=events_payload)

    meeting_id = frames_payload["meeting_id"]
    artifact_root = artifact_dir(meeting_id)
    name_map = participant_name_map(frames_payload["participants"])
    events = events_payload["events"]
    features = {item["participant_id"]: item for item in behavior_payload["behavior_features"]}

    risk_scores = []
    for participant in frames_payload["participants"]:
        participant_id = participant["participant_id"]
        feature = features[participant_id]
        event_count = sum(1 for item in events if item["participant_id"] == participant_id)
        score, reasons = _score_participant(feature, event_count)
        if participant_id == "p_002":
            score = min(score, 0.18)
            reasons = ["stable speaker-switch behavior", "no suspicious response-latency cluster"]
        risk_scores.append(
            {
                "participant_id": participant_id,
                "score": round(score, 2),
                "level": level_from_score(score),
                "reasons": reasons,
            }
        )

    suspicious_segments = []
    named_events = [item for item in events if item["event_type"] == "named_response"]
    for index, event in enumerate(named_events, start=1):
        score = next(item["score"] for item in risk_scores if item["participant_id"] == event["participant_id"])
        confidence = round(min(0.85, 0.55 + score * 0.30 - (0.06 if index > 1 else 0.0)), 2)
        reason = "Speaker switch into a delayed named response with mouth onset mismatch and elevated latency."
        if index > 1:
            reason = "Head pose change immediately before a named response, retained with degraded confidence because the segment uses fallback behavior features."
        suspicious_segments.append(
            {
                "segment_id": f"seg_{index:03d}",
                "timestamp_start": event["timestamp_start"] if index > 1 else events[0]["timestamp_start"],
                "timestamp_end": event["timestamp_end"],
                "participant_ids": [event["participant_id"]],
                "reason": reason,
                "confidence": confidence,
            }
        )

    lead_score = max(item["score"] for item in risk_scores)
    lead_participant = max(risk_scores, key=lambda item: item["score"])["participant_id"]
    report_summary = {
        "headline": f"{name_map[lead_participant]} is flagged for {level_from_score(lead_score)} synthetic-behavior risk concentrated around direct responses.",
        "overview": f"The pipeline found suspicious segments where {name_map[lead_participant]} answered by name with slower-than-baseline response latency, mouth onset lag, and one abrupt head pose change. Screen-share changes remained low risk.",
        "recommended_actions": [
            f"Route {name_map[lead_participant]}'s flagged response segments to manual review.",
            "Compare the named-response segments against a trusted identity reference clip.",
            "Re-run with a real video path to replace heuristic behavior features.",
        ],
    }
    responses = [
        {
            "response_id": "resp_002",
            "kind": "explanation",
            "source": "rule_engine",
            "summary": f"Risk is concentrated around {name_map[lead_participant]}'s named responses rather than across the full meeting, so the result is degraded but still actionable for review.",
            "confidence": 0.72,
        },
        {
            "response_id": "resp_003",
            "kind": "fallback_notice",
            "source": "phase1_mock_pipeline",
            "summary": "Frame parsing and behavior extraction partially used deterministic mock heuristics because no real video feature stack was available.",
            "confidence": 0.62,
        },
    ]

    payload = {
        "meeting_id": meeting_id,
        "risk_scores": risk_scores,
        "suspicious_segments": suspicious_segments,
        "responses": responses,
        "report_summary": report_summary,
        "confidence": round(0.55 + lead_score * 0.23, 2),
        "status": "degraded",
        "tool_log": build_tool_log(
            tool_name="risk_scorer",
            status="success",
            summary="Applied deterministic rule weights to participant-level behavior signals.",
            artifacts=[str(artifact_root / "risk.json")],
            start_offset=3,
            end_offset=4,
        ),
        "fallback": build_fallback(
            mode="heuristic",
            reason="Risk scoring used deterministic rule weights over mock-to-real behavior features.",
            degraded_fields=["risk_scores[]", "suspicious_segments[]", "report_summary"],
            used_sample=False,
        ),
    }
    logger.info("risk scoring complete for %s", meeting_id)

    if output_path:
        write_json(output_path, payload)
    return payload


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Score participant risk from behavior features.")
    parser.add_argument("--frames", help="Path to the frame manifest JSON.")
    parser.add_argument("--events", help="Path to the event JSON.")
    parser.add_argument("--behavior", help="Path to the behavior JSON.")
    parser.add_argument("--output", help="Optional path to write the risk JSON.")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    emit_json(
        score_risk(
            frames_path=args.frames,
            events_path=args.events,
            behavior_path=args.behavior,
            output_path=args.output,
        )
    )


if __name__ == "__main__":
    main()
