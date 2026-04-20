from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SAMPLE_RESULT_PATH = ROOT / "demo" / "sample_json" / "sample_result.json"

REQUIRED_TOP_LEVEL_FIELDS = {
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
}

P0_EVENT_TYPES = {"speaker_switch", "named_response", "screen_share_change"}


def load_sample() -> dict:
    return json.loads(SAMPLE_RESULT_PATH.read_text(encoding="utf-8"))


def run_pipeline(*args: str) -> dict:
    result = subprocess.run(
        [sys.executable, "backend/pipelines/run_pipeline.py", *args],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    start = result.stdout.find("{")
    if start < 0:
        raise AssertionError(result.stdout)
    return json.loads(result.stdout[start:])


class PipelineContractTest(unittest.TestCase):
    def test_sample_result_has_required_top_level_fields(self) -> None:
        payload = load_sample()
        self.assertTrue(REQUIRED_TOP_LEVEL_FIELDS.issubset(payload))
        self.assertTrue(payload["validation"]["schema_valid"])
        self.assertTrue(payload["responses"])

    def test_sample_result_covers_p0_event_types(self) -> None:
        payload = load_sample()
        event_types = {item["event_type"] for item in payload["events"]}
        self.assertTrue(P0_EVENT_TYPES.issubset(event_types))

    def test_run_pipeline_sample_mode_is_contract_aligned(self) -> None:
        payload = run_pipeline("--use-sample")
        self.assertTrue(REQUIRED_TOP_LEVEL_FIELDS.issubset(payload))
        self.assertTrue(payload["fallback"]["used_sample"])
        self.assertTrue(payload["validation"]["schema_valid"])

    def test_run_pipeline_heuristic_mode_writes_complete_result(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            video_path = Path(temp_dir) / "meeting.mp4"
            video_path.write_bytes(b"demo")
            output_path = Path(temp_dir) / "result.json"
            payload = run_pipeline(
                "--video-path",
                str(video_path),
                "--meeting-id",
                "meeting_test_cli",
                "--output",
                str(output_path),
            )

            self.assertEqual(payload["meeting_id"], "meeting_test_cli")
            self.assertEqual(payload["status"], "degraded")
            self.assertIn(payload["fallback"]["mode"], {"heuristic", "hybrid_fallback"})
            self.assertTrue(payload["validation"]["schema_valid"])
            self.assertTrue(output_path.exists())


if __name__ == "__main__":
    unittest.main()
