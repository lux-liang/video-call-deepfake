from __future__ import annotations

import asyncio
import unittest

from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError

from app.core.errors import AppError, app_error_handler, request_validation_error_handler
from app.api.routes.health import health
from app.main import create_app
from app.schemas.analysis import AnalyzeRequest, UploadRequest
from app.services.analysis_service import AnalysisService
from app.services.report_service import ReportService
from app.services.task_store import TaskStore


class MeetTruthBackendTests(unittest.TestCase):
    def setUp(self) -> None:
        self.app = create_app()
        self.service = AnalysisService(
            task_store=TaskStore(),
            report_service=ReportService(),
        )

    def test_app_registers_required_routes(self) -> None:
        paths = {(route.path, tuple(sorted(route.methods or []))) for route in self.app.routes}
        self.assertIn(("/health", ("GET",)), paths)
        self.assertIn(("/healthz", ("GET",)), paths)
        self.assertIn(("/api/demo/sample-result", ("GET",)), paths)
        self.assertIn(("/api/upload", ("POST",)), paths)
        self.assertIn(("/api/analyze", ("POST",)), paths)
        self.assertIn(("/api/task/{task_id}", ("GET",)), paths)
        self.assertIn(("/api/result/{task_id}", ("GET",)), paths)
        self.assertIn(("/api/report/{task_id}", ("GET",)), paths)

    def test_health_handler_returns_expected_payload(self) -> None:
        payload = health().model_dump(mode="json")
        self.assertEqual(payload["status"], "ok")
        self.assertEqual(payload["service"], "meettruth-backend")
        self.assertEqual(payload["version"], "0.2.0")

    def test_sample_result_endpoint_contract_via_service(self) -> None:
        result = self.service.get_demo_sample_result()
        payload = result.model_dump(mode="json")
        self.assertEqual(payload["status"], "completed")
        self.assertEqual(payload["fallback"]["mode"], "sample")
        self.assertIsInstance(payload["participants"], list)
        self.assertIsInstance(payload["events"], list)
        self.assertIsInstance(payload["responses"], list)
        self.assertIsInstance(payload["risk_scores"], list)
        self.assertIsInstance(payload["suspicious_segments"], list)
        self.assertIsInstance(payload["tool_logs"], list)
        self.assertEqual(payload["validation"]["validator_version"], "phase1-p0")

    def test_upload_request_validation_rejects_non_video_inputs(self) -> None:
        with self.assertRaises(ValidationError):
            UploadRequest(filename="notes.txt", content_type="text/plain", source="local_upload")

    def test_analyze_flow_returns_result_task_and_report(self) -> None:
        upload = self.service.create_upload(
            UploadRequest(
                filename="team-sync.mp4",
                content_type="video/mp4",
                source="local_upload",
            )
        )

        pending = self.service.get_result(upload.task_id).model_dump(mode="json")
        self.assertEqual(pending["status"], "queued")
        self.assertEqual(pending["fallback"]["mode"], "pending")

        analyze = self.service.start_analysis(
            AnalyzeRequest(
                meeting_id=upload.meeting_id,
                upload_id=upload.upload_id,
                mode="playback_mock",
                use_mock=True,
            )
        )
        self.assertEqual(analyze.status, "processing")

        task = self.service.get_task_status(upload.task_id).model_dump(mode="json")
        self.assertEqual(task["status"], "completed")
        self.assertEqual(task["progress"], 100)
        self.assertEqual(task["stage"], "reporting")
        self.assertIsNone(task["error"])

        result = self.service.get_result(upload.task_id).model_dump(mode="json")
        self.assertEqual(result["meeting_id"], upload.meeting_id)
        self.assertEqual(result["status"], "completed")
        self.assertEqual(result["fallback"]["mode"], "playback_mock")
        self.assertGreater(len(result["responses"]), 0)

        report = self.service.get_report(upload.task_id).model_dump(mode="json")
        self.assertEqual(report["status"], "completed")
        self.assertIn(upload.meeting_id, report["report_markdown"])

    def test_pipeline_real_mode_degrades_to_sample_fallback(self) -> None:
        upload = self.service.create_upload(
            UploadRequest(
                filename="team-sync.mp4",
                content_type="video/mp4",
                source="local_upload",
            )
        )

        self.service.start_analysis(
            AnalyzeRequest(
                meeting_id=upload.meeting_id,
                upload_id=upload.upload_id,
                mode="pipeline_real",
                use_mock=False,
            )
        )

        task = self.service.get_task_status(upload.task_id).model_dump(mode="json")
        self.assertEqual(task["status"], "degraded")
        self.assertIsNotNone(task["error"])

        result = self.service.get_result(upload.task_id).model_dump(mode="json")
        self.assertEqual(result["status"], "degraded")
        self.assertLessEqual(result["confidence"], 0.35)
        self.assertEqual(result["fallback"]["mode"], "sample_mock_fallback")
        self.assertFalse(result["validation"]["schema_valid"])
        self.assertGreater(len(result["validation"]["missing_fields"]), 0)
        self.assertGreater(len(result["responses"]), 0)
        self.assertGreater(len(result["tool_logs"]), 0)

    def test_missing_task_raises_app_error(self) -> None:
        with self.assertRaises(AppError) as ctx:
            self.service.get_task_status("task_missing")
        self.assertEqual(ctx.exception.code, "task_not_found")

    def test_request_validation_handler_returns_stable_error_shape(self) -> None:
        request_error = RequestValidationError(
            [
                {
                    "type": "value_error",
                    "loc": ("body", "filename"),
                    "msg": "Value error, filename must end with one of: .mp4",
                    "input": "bad.txt",
                    "ctx": {"error": "bad extension"},
                }
            ]
        )
        response = asyncio.run(request_validation_error_handler(None, request_error))
        payload = response.body.decode()
        self.assertEqual(response.status_code, 422)
        self.assertIn('"status":"failed"', payload)
        self.assertIn('"code":"request_validation_error"', payload)
        self.assertIn('"field":"filename"', payload)

    def test_app_error_handler_returns_stable_error_shape(self) -> None:
        response = asyncio.run(
            app_error_handler(
                None,
                AppError(
                    status_code=404,
                    code="task_not_found",
                    message="task 'task_missing' was not found",
                ),
            )
        )
        payload = response.body.decode()
        self.assertEqual(response.status_code, 404)
        self.assertIn('"status":"failed"', payload)
        self.assertIn('"code":"task_not_found"', payload)


if __name__ == "__main__":
    unittest.main()
