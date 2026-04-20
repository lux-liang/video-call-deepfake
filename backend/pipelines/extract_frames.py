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
        default_meeting_id,
        derive_timeline,
        deterministic_int,
        emit_json,
        participant_templates,
        write_json,
    )
else:
    from .common import (
        artifact_dir,
        build_fallback,
        build_tool_log,
        configure_logging,
        default_meeting_id,
        derive_timeline,
        deterministic_int,
        emit_json,
        participant_templates,
        write_json,
    )


def extract_frames(
    video_path: str | None = None,
    meeting_id: str | None = None,
    output_path: str | Path | None = None,
) -> dict[str, Any]:
    logger = configure_logging("extract_frames")
    resolved_meeting_id = meeting_id or default_meeting_id(video_path)
    artifact_root = artifact_dir(resolved_meeting_id)

    path = Path(video_path) if video_path else None
    if path and path.exists():
        file_size = path.stat().st_size
        duration_seconds = round(90.0 + float(file_size % 48), 1)
        source_mode = "heuristic_video"
        tool_status = "degraded"
        tool_summary = "Video metadata was probed and converted into a deterministic frame manifest without ffmpeg."
        fallback = build_fallback(
            mode="heuristic",
            reason="No real ffmpeg/OpenCV stack is connected in Phase 1, so frame extraction uses deterministic file-metadata heuristics.",
            degraded_fields=["tool_logs[]"],
            used_sample=False,
        )
    else:
        duration_seconds = round(118.0 + float(deterministic_int(resolved_meeting_id) % 10), 1)
        source_mode = "mock"
        tool_status = "mocked"
        tool_summary = "Synthetic frame manifest generated because no usable video path was provided."
        fallback = build_fallback(
            mode="mock",
            reason="No input video was available, so the frame stage emitted a stable demo manifest.",
            degraded_fields=["frames[]", "tool_logs[]"],
            used_sample=True,
        )

    timeline = derive_timeline(resolved_meeting_id, duration_seconds)
    payload = {
        "meeting_id": resolved_meeting_id,
        "source_mode": source_mode,
        "source_video": str(path) if path and path.exists() else None,
        "duration_seconds": timeline["duration_seconds"],
        "frames": timeline["frames"],
        "participants": participant_templates(),
        "speaker_turns": timeline["speaker_turns"],
        "screen_share_windows": timeline["screen_share_windows"],
        "tool_log": build_tool_log(
            tool_name="extract_frames",
            status=tool_status,
            summary=tool_summary,
            artifacts=[str(artifact_root / "frames.json")],
            start_offset=0,
            end_offset=1,
        ),
        "fallback": fallback,
    }
    logger.info("frame manifest ready for %s in %s mode", resolved_meeting_id, source_mode)

    if output_path:
        write_json(output_path, payload)
    return payload


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Create a minimal frame manifest for the meeting pipeline.")
    parser.add_argument("--video-path", help="Path to the input video. When missing, a mock manifest is emitted.")
    parser.add_argument("--meeting-id", help="Optional meeting id override.")
    parser.add_argument("--output", help="Optional path to write the frame manifest JSON.")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    emit_json(extract_frames(video_path=args.video_path, meeting_id=args.meeting_id, output_path=args.output))


if __name__ == "__main__":
    main()
