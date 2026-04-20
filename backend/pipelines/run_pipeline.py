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
        build_validation,
        configure_logging,
        default_meeting_id,
        emit_json,
        merge_unique,
        result_for_meeting,
        write_json,
    )
    from backend.pipelines.detect_events import detect_events
    from backend.pipelines.extract_behavior import extract_behavior
    from backend.pipelines.extract_frames import extract_frames
    from backend.pipelines.score_risk import score_risk
else:
    from .common import (
        artifact_dir,
        build_fallback,
        build_validation,
        configure_logging,
        default_meeting_id,
        emit_json,
        merge_unique,
        result_for_meeting,
        write_json,
    )
    from .detect_events import detect_events
    from .extract_behavior import extract_behavior
    from .extract_frames import extract_frames
    from .score_risk import score_risk


def _fallback_result(meeting_id: str, reason: str, degraded_fields: list[str], used_sample: bool) -> dict[str, Any]:
    payload = result_for_meeting(meeting_id)
    payload["status"] = "degraded"
    payload["confidence"] = min(payload["confidence"], 0.72)
    payload["fallback"] = build_fallback(
        mode="mock" if used_sample else "heuristic",
        reason=reason,
        degraded_fields=merge_unique(payload["fallback"].get("degraded_fields", []) + degraded_fields),
        used_sample=used_sample,
    )
    validation = build_validation(payload, warnings=payload.get("validation", {}).get("warnings", []))
    payload["validation"] = validation
    return payload


def _finalize_participants(
    participants: list[dict[str, Any]],
    risk_scores: list[dict[str, Any]],
    behavior_features: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    risk_map = {item["participant_id"]: item for item in risk_scores}
    behavior_map = {item["participant_id"]: item for item in behavior_features}
    finalized = []
    for participant in participants:
        participant_id = participant["participant_id"]
        risk = risk_map[participant_id]
        behavior = behavior_map[participant_id]
        notes = participant["notes"]
        if participant_id == "p_001":
            notes = "Frequent response latency spikes and repeated mouth-onset mismatches during named responses."
            if behavior["head_pose_change"]["count"]:
                notes += " One response also includes an abrupt head pose change."
        elif risk["level"] == "low":
            notes = "Stable speaking cadence with no high-severity event cluster."
        finalized.append(
            {
                **participant,
                "dominant_risk_level": risk["level"],
                "notes": notes,
            }
        )
    return finalized


def run_pipeline(
    video_path: str | None = None,
    meeting_id: str | None = None,
    output_path: str | Path | None = None,
    use_sample: bool = False,
) -> dict[str, Any]:
    logger = configure_logging("run_pipeline")
    resolved_meeting_id = meeting_id or default_meeting_id(video_path)

    if use_sample or not video_path:
        reason = "No real video path was provided, so the pipeline returned the stable demo sample result."
        payload = _fallback_result(
            meeting_id=resolved_meeting_id,
            reason=reason,
            degraded_fields=["tool_logs[]"],
            used_sample=True,
        )
        if output_path:
            write_json(output_path, payload)
        logger.info("returned sample result for %s", resolved_meeting_id)
        return payload

    path = Path(video_path)
    if not path.exists():
        payload = _fallback_result(
            meeting_id=resolved_meeting_id,
            reason=f"Input video path does not exist: {video_path}. Falling back to the stable demo sample result.",
            degraded_fields=["tool_logs[]"],
            used_sample=True,
        )
        if output_path:
            write_json(output_path, payload)
        logger.warning("video path missing for %s, used sample fallback", resolved_meeting_id)
        return payload

    stage_dir = artifact_dir(resolved_meeting_id)
    warnings: list[str] = []
    used_sample = False

    try:
        frames_payload = extract_frames(video_path=video_path, meeting_id=resolved_meeting_id, output_path=stage_dir / "frames.json")
    except Exception as exc:
        logger.exception("frame extraction failed for %s", resolved_meeting_id)
        return _fallback_result(
            meeting_id=resolved_meeting_id,
            reason=f"Frame extraction failed with {exc.__class__.__name__}. Returned stable demo sample.",
            degraded_fields=["events[]", "responses[]", "risk_scores[]", "suspicious_segments[]", "tool_logs[]"],
            used_sample=True,
        )

    try:
        events_payload = detect_events(frames_payload=frames_payload, output_path=stage_dir / "events.json")
    except Exception as exc:
        logger.exception("event detection failed for %s", resolved_meeting_id)
        sample = result_for_meeting(resolved_meeting_id)
        events_payload = {
            "meeting_id": resolved_meeting_id,
            "participants": frames_payload["participants"],
            "events": sample["events"],
            "tool_log": {
                "tool_name": "event_detector",
                "status": "degraded",
                "started_at": frames_payload["tool_log"]["ended_at"],
                "ended_at": frames_payload["tool_log"]["ended_at"],
                "summary": f"Event detection failed with {exc.__class__.__name__}; sample events were reused.",
                "artifacts": [str(stage_dir / "events.json")],
            },
            "fallback": build_fallback(
                mode="sample_event_fallback",
                reason=f"Event detection failed with {exc.__class__.__name__}. Sample events were injected.",
                degraded_fields=["events[]"],
                used_sample=True,
            ),
        }
        write_json(stage_dir / "events.json", events_payload)
        warnings.append(events_payload["fallback"]["reason"])
        used_sample = True

    try:
        behavior_payload = extract_behavior(
            frames_payload=frames_payload,
            events_payload=events_payload,
            output_path=stage_dir / "behavior.json",
        )
    except Exception as exc:
        logger.exception("behavior extraction failed for %s", resolved_meeting_id)
        sample = result_for_meeting(resolved_meeting_id)
        behavior_payload = {
            "meeting_id": resolved_meeting_id,
            "participants": frames_payload["participants"],
            "behavior_features": [
                {
                    "participant_id": "p_001",
                    "mouth_onset": {"count": 1, "avg_delay_seconds": 0.3, "max_delay_seconds": 0.3, "severity": "medium"},
                    "head_pose_change": {"count": 0, "max_delta_degrees": 0.0, "severity": "low"},
                    "response_latency": {"count": 1, "avg_seconds": 2.3, "baseline_seconds": 1.1, "severity": "medium"},
                    "notes": sample["responses"][0]["summary"],
                },
                {
                    "participant_id": "p_002",
                    "mouth_onset": {"count": 0, "avg_delay_seconds": 0.0, "max_delay_seconds": 0.0, "severity": "low"},
                    "head_pose_change": {"count": 0, "max_delta_degrees": 0.0, "severity": "low"},
                    "response_latency": {"count": 0, "avg_seconds": 0.9, "baseline_seconds": 0.9, "severity": "low"},
                    "notes": "Behavior extraction fallback used for the secondary participant.",
                },
            ],
            "responses": sample["responses"][:1],
            "tool_log": {
                "tool_name": "behavior_extractor",
                "status": "degraded",
                "started_at": events_payload["tool_log"]["ended_at"],
                "ended_at": events_payload["tool_log"]["ended_at"],
                "summary": f"Behavior extraction failed with {exc.__class__.__name__}; fallback heuristics were injected.",
                "artifacts": [str(stage_dir / "behavior.json")],
            },
            "fallback": build_fallback(
                mode="heuristic_fallback",
                reason=f"Behavior extraction failed with {exc.__class__.__name__}. Simplified heuristics were injected.",
                degraded_fields=["responses[]", "risk_scores[]", "suspicious_segments[]"],
                used_sample=False,
            ),
        }
        write_json(stage_dir / "behavior.json", behavior_payload)
        warnings.append(behavior_payload["fallback"]["reason"])

    try:
        score_payload = score_risk(
            frames_payload=frames_payload,
            events_payload=events_payload,
            behavior_payload=behavior_payload,
            output_path=stage_dir / "risk.json",
        )
    except Exception as exc:
        logger.exception("risk scoring failed for %s", resolved_meeting_id)
        sample = result_for_meeting(resolved_meeting_id)
        score_payload = {
            "meeting_id": resolved_meeting_id,
            "risk_scores": sample["risk_scores"],
            "suspicious_segments": sample["suspicious_segments"],
            "responses": sample["responses"][1:],
            "report_summary": sample["report_summary"],
            "confidence": 0.58,
            "status": "degraded",
            "tool_log": {
                "tool_name": "risk_scorer",
                "status": "degraded",
                "started_at": behavior_payload["tool_log"]["ended_at"],
                "ended_at": behavior_payload["tool_log"]["ended_at"],
                "summary": f"Risk scoring failed with {exc.__class__.__name__}; sample scoring output was reused.",
                "artifacts": [str(stage_dir / "risk.json")],
            },
            "fallback": build_fallback(
                mode="sample_score_fallback",
                reason=f"Risk scoring failed with {exc.__class__.__name__}. Sample score output was injected.",
                degraded_fields=["risk_scores[]", "suspicious_segments[]", "report_summary"],
                used_sample=True,
            ),
        }
        write_json(stage_dir / "risk.json", score_payload)
        warnings.append(score_payload["fallback"]["reason"])
        used_sample = True

    responses = behavior_payload["responses"] + score_payload["responses"]
    fallback_reason = "Heuristic frame probing, event detection, and behavior scoring were used because the real tool stack is not yet connected."
    if used_sample:
        fallback_reason += " Some stages also reused stable sample content after a failure."
    fallback = build_fallback(
        mode="heuristic" if not used_sample else "hybrid_fallback",
        reason=fallback_reason,
        degraded_fields=merge_unique(
            frames_payload["fallback"]["degraded_fields"]
            + events_payload["fallback"]["degraded_fields"]
            + behavior_payload["fallback"]["degraded_fields"]
            + score_payload["fallback"]["degraded_fields"]
        ),
        used_sample=used_sample,
    )

    payload = {
        "meeting_id": resolved_meeting_id,
        "status": score_payload["status"],
        "confidence": score_payload["confidence"],
        "participants": _finalize_participants(
            participants=frames_payload["participants"],
            risk_scores=score_payload["risk_scores"],
            behavior_features=behavior_payload["behavior_features"],
        ),
        "events": events_payload["events"],
        "responses": responses,
        "risk_scores": score_payload["risk_scores"],
        "suspicious_segments": score_payload["suspicious_segments"],
        "tool_logs": [
            frames_payload["tool_log"],
            events_payload["tool_log"],
            behavior_payload["tool_log"],
            score_payload["tool_log"],
        ],
        "report_summary": score_payload["report_summary"],
        "validation": {},
        "fallback": fallback,
    }
    validation = build_validation(
        payload,
        warnings=warnings + ["Behavior features were produced by heuristic fallback logic."],
    )
    payload["validation"] = validation

    final_output = Path(output_path) if output_path else stage_dir / "result.json"
    write_json(final_output, payload)
    logger.info("pipeline result written to %s", final_output)
    return payload


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run the minimal meeting replay to JSON pipeline.")
    parser.add_argument("--video-path", help="Path to the input video. When omitted, the stable sample result is returned.")
    parser.add_argument("--meeting-id", help="Optional meeting id override.")
    parser.add_argument("--output", help="Optional path to write the final pipeline result JSON.")
    parser.add_argument("--use-sample", action="store_true", help="Force the pipeline to return the stable sample result.")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    emit_json(
        run_pipeline(
            video_path=args.video_path,
            meeting_id=args.meeting_id,
            output_path=args.output,
            use_sample=args.use_sample,
        )
    )


if __name__ == "__main__":
    main()
