from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timezone
from typing import Any

from pydantic import ValidationError

from app.core.errors import AppError
from app.schemas.analysis import (
    AnalysisResult,
    AnalyzeMode,
    AnalyzeRequest,
    AnalyzeResponse,
    FallbackInfo,
    ReportResponse,
    ReportSummary,
    StructuredResponse,
    TaskStatus,
    TaskStatusResponse,
    ToolLog,
    ToolLogStatus,
    UploadRequest,
    UploadResponse,
    ValidationInfo,
)
from app.services.report_service import ReportService
from app.services.sample_data import build_sample_result
from app.services.task_store import TaskRecord, TaskStore, UploadRecord, utcnow


REQUIRED_RESULT_FIELDS = (
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


def isoformat(value: datetime) -> str:
    return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


class AnalysisService:
    def __init__(self, *, task_store: TaskStore, report_service: ReportService) -> None:
        self._task_store = task_store
        self._report_service = report_service

    def get_demo_sample_result(self) -> AnalysisResult:
        payload = build_sample_result(
            meeting_id="meeting_demo_001",
            status=TaskStatus.COMPLETED.value,
            confidence=0.78,
            mode=AnalyzeMode.SAMPLE.value,
            reason="sample result endpoint",
            used_sample=True,
        )
        result = AnalysisResult.model_validate(payload)
        return self._ensure_result_notice(
            result,
            mode=AnalyzeMode.SAMPLE.value,
            warning="Sample result endpoint returned canonical Phase 1 sample output.",
        )

    def create_upload(self, payload: UploadRequest) -> UploadResponse:
        upload, task = self._task_store.create_upload(payload)
        return UploadResponse(
            task_id=task.task_id,
            meeting_id=task.meeting_id,
            upload_id=upload.upload_id,
            status=task.status,
            message=f"upload accepted for {payload.filename}",
        )

    def start_analysis(self, payload: AnalyzeRequest) -> AnalyzeResponse:
        upload = self._task_store.get_upload(payload.upload_id)
        if upload.meeting_id != payload.meeting_id:
            raise AppError(
                status_code=400,
                code="meeting_upload_mismatch",
                message="meeting_id does not match the upload record",
            )

        task = self._task_store.update_task(
            upload.task_id,
            status=TaskStatus.PROCESSING,
            progress=15,
            stage="pipeline_dispatch",
            confidence=0.05,
            error=None,
            requested_mode=payload.mode.value,
            use_mock=payload.use_mock,
        )

        final_result = self._run_analysis(upload=upload, payload=payload)
        report_markdown = self._report_service.build_report(
            task_id=task.task_id,
            result=final_result,
        )
        self._task_store.update_task(
            task.task_id,
            status=final_result.status,
            progress=100,
            stage="reporting",
            confidence=final_result.confidence,
            error=self._build_task_error(final_result),
            result=final_result,
            report_markdown=report_markdown,
        )

        return AnalyzeResponse(
            task_id=task.task_id,
            meeting_id=task.meeting_id,
            status=TaskStatus.PROCESSING,
            estimated_mode=payload.mode.value,
        )

    def get_task_status(self, task_id: str) -> TaskStatusResponse:
        task = self._task_store.get_task(task_id)
        return TaskStatusResponse(
            task_id=task.task_id,
            meeting_id=task.meeting_id,
            status=task.status,
            progress=task.progress,
            stage=task.stage,
            confidence=task.confidence,
            error=task.error,
        )

    def get_result(self, task_id: str) -> AnalysisResult:
        task = self._task_store.get_task(task_id)
        if task.result is not None:
            return task.result
        return self._build_pending_result(task)

    def get_report(self, task_id: str) -> ReportResponse:
        task = self._task_store.get_task(task_id)
        if task.report_markdown is not None:
            report_markdown = task.report_markdown
        else:
            report_markdown = self._report_service.build_pending_report(
                task_id=task.task_id,
                meeting_id=task.meeting_id,
                status=task.status,
            )
        return ReportResponse(
            task_id=task.task_id,
            meeting_id=task.meeting_id,
            status=task.status,
            report_markdown=report_markdown,
            generated_at=task.updated_at,
        )

    def _run_analysis(self, *, upload: UploadRecord, payload: AnalyzeRequest) -> AnalysisResult:
        try:
            if payload.use_mock or payload.mode in {AnalyzeMode.PLAYBACK_MOCK, AnalyzeMode.SAMPLE}:
                raw_result = self._run_mock_pipeline(upload=upload, payload=payload)
            else:
                raw_result = self._run_real_pipeline_placeholder(upload=upload, payload=payload)
            return self._normalize_pipeline_result(
                raw_result=raw_result,
                meeting_id=upload.meeting_id,
                requested_mode=payload.mode.value,
                requested_use_mock=payload.use_mock,
            )
        except AppError:
            raise
        except Exception as exc:
            return self._build_sample_fallback(
                meeting_id=upload.meeting_id,
                requested_mode=payload.mode.value,
                reason=f"analysis execution failed: {exc}",
                degraded_fields=["analysis_execution"],
                raw_payload=None,
            )

    def _run_mock_pipeline(self, *, upload: UploadRecord, payload: AnalyzeRequest) -> dict[str, Any]:
        mode = payload.mode.value
        if payload.mode == AnalyzeMode.PLAYBACK_MOCK:
            reason = "mock analysis requested by caller"
        else:
            reason = "sample analysis requested by caller"

        result = build_sample_result(
            meeting_id=upload.meeting_id,
            status=TaskStatus.COMPLETED.value,
            confidence=0.78,
            mode=mode,
            reason=reason,
            used_sample=True,
        )
        return self._append_result_notice(
            payload=result,
            summary=f"Analysis completed in `{mode}` using sample/mock Phase 1 data.",
            confidence=0.6,
        )

    def _run_real_pipeline_placeholder(
        self,
        *,
        upload: UploadRecord,
        payload: AnalyzeRequest,
    ) -> dict[str, Any]:
        started_at = utcnow()
        finished_at = utcnow()
        return {
            "meeting_id": upload.meeting_id,
            "status": TaskStatus.DEGRADED.value,
            "confidence": 0.18,
            "responses": [
                {
                    "response_id": "resp_pipeline_unavailable",
                    "kind": "fallback_notice",
                    "source": "pipeline_adapter",
                    "summary": "Real pipeline adapter is not connected in Phase 1. Backend will degrade to a sample-backed result.",
                    "confidence": 0.2,
                }
            ],
            "tool_logs": [
                {
                    "tool_name": "pipeline_adapter",
                    "status": ToolLogStatus.FAILED.value,
                    "started_at": isoformat(started_at),
                    "ended_at": isoformat(finished_at),
                    "summary": f"Mode `{payload.mode.value}` is not connected yet. Returning incomplete placeholder payload for fallback handling.",
                    "artifacts": [],
                }
            ],
            "fallback": {
                "mode": payload.mode.value,
                "reason": "real pipeline adapter not connected",
                "degraded_fields": [
                    "participants",
                    "events",
                    "risk_scores",
                    "suspicious_segments",
                    "report_summary",
                    "validation",
                ],
                "used_sample": False,
            },
        }

    def _normalize_pipeline_result(
        self,
        *,
        raw_result: dict[str, Any],
        meeting_id: str,
        requested_mode: str,
        requested_use_mock: bool,
    ) -> AnalysisResult:
        payload = deepcopy(raw_result)
        payload["meeting_id"] = meeting_id
        missing_fields = [field for field in REQUIRED_RESULT_FIELDS if field not in payload]

        if missing_fields:
            return self._build_sample_fallback(
                meeting_id=meeting_id,
                requested_mode=requested_mode,
                reason="pipeline payload missing required contract fields",
                degraded_fields=missing_fields,
                raw_payload=payload,
            )

        try:
            result = AnalysisResult.model_validate(payload)
        except ValidationError as exc:
            return self._build_sample_fallback(
                meeting_id=meeting_id,
                requested_mode=requested_mode,
                reason="pipeline payload failed schema validation",
                degraded_fields=self._validation_error_fields(exc),
                raw_payload=payload,
            )

        warning = (
            "Sample/mock data was used because the caller explicitly requested mock mode."
            if requested_use_mock
            else "Result completed without contract degradation."
        )
        return self._ensure_result_notice(result, mode=requested_mode, warning=warning)

    def _build_sample_fallback(
        self,
        *,
        meeting_id: str,
        requested_mode: str,
        reason: str,
        degraded_fields: list[str],
        raw_payload: dict[str, Any] | None,
    ) -> AnalysisResult:
        confidence = 0.2
        raw_responses = []
        raw_tool_logs = []

        if isinstance(raw_payload, dict):
            confidence = float(raw_payload.get("confidence", confidence) or confidence)
            raw_responses = self._sanitize_responses(raw_payload.get("responses", []))
            raw_tool_logs = self._sanitize_tool_logs(raw_payload.get("tool_logs", []))

        sample_payload = build_sample_result(
            meeting_id=meeting_id,
            status=TaskStatus.DEGRADED.value,
            confidence=min(confidence, 0.35),
            mode="sample_mock_fallback",
            reason=reason,
            used_sample=True,
        )
        sample_payload["validation"] = {
            "schema_valid": False,
            "missing_fields": sorted(set(degraded_fields)),
            "warnings": [
                "Backend returned a sample-backed fallback result because the real pipeline payload was incomplete or invalid.",
            ],
            "validator_version": "phase1-p0",
        }
        sample_payload["fallback"] = {
            "mode": "sample_mock_fallback",
            "reason": f"{reason} while handling requested mode `{requested_mode}`",
            "degraded_fields": sorted(set(degraded_fields)),
            "used_sample": True,
        }

        if raw_responses:
            sample_payload["responses"] = list(raw_responses) + sample_payload["responses"]
        sample_payload = self._append_result_notice(
            payload=sample_payload,
            summary=(
                "Backend degraded to sample/mock output after validation detected missing or invalid pipeline fields."
            ),
            confidence=0.24,
        )

        if raw_tool_logs:
            sample_payload["tool_logs"] = list(raw_tool_logs) + sample_payload["tool_logs"]

        result = AnalysisResult.model_validate(sample_payload)
        return self._ensure_result_notice(
            result,
            mode="sample_mock_fallback",
            warning="Result was downgraded to sample/mock output to preserve a stable response schema.",
        )

    def _build_pending_result(self, task: TaskRecord) -> AnalysisResult:
        return AnalysisResult(
            meeting_id=task.meeting_id,
            status=task.status,
            confidence=task.confidence,
            participants=[],
            events=[],
            responses=[
                StructuredResponse(
                    response_id="resp_pending",
                    kind="status_notice",
                    source="backend_state",
                    summary=f"Analysis is currently `{task.status}`. Poll the task endpoint until completion.",
                    confidence=0.1,
                )
            ],
            risk_scores=[],
            suspicious_segments=[],
            tool_logs=[],
            report_summary=ReportSummary(
                headline="Analysis not ready",
                overview="The result is still being prepared.",
                recommended_actions=[],
            ),
            validation=ValidationInfo(
                schema_valid=True,
                warnings=["A placeholder result was returned because the task is not finalized yet."],
            ),
            fallback=FallbackInfo(
                mode="pending",
                reason="analysis has not completed yet",
                degraded_fields=[
                    "participants",
                    "events",
                    "risk_scores",
                    "suspicious_segments",
                    "tool_logs",
                ],
                used_sample=False,
            ),
        )

    def _ensure_result_notice(
        self,
        result: AnalysisResult,
        *,
        mode: str,
        warning: str,
    ) -> AnalysisResult:
        payload = result.model_dump(mode="python")
        warnings = payload["validation"]["warnings"]
        if warning not in warnings:
            warnings.append(warning)
        payload["validation"]["validator_version"] = "phase1-p0"
        if payload["fallback"]["mode"] == "mock":
            payload["fallback"]["mode"] = mode
        return AnalysisResult.model_validate(payload)

    def _append_result_notice(
        self,
        *,
        payload: dict[str, Any],
        summary: str,
        confidence: float,
    ) -> dict[str, Any]:
        notices = list(payload.get("responses", []))
        notices.append(
            {
                "response_id": f"resp_notice_{len(notices) + 1:03d}",
                "kind": "fallback_notice",
                "source": "backend_service",
                "summary": summary,
                "confidence": confidence,
            }
        )
        payload["responses"] = notices
        return payload

    @staticmethod
    def _validation_error_fields(exc: ValidationError) -> list[str]:
        return sorted(
            {
                ".".join(str(part) for part in error["loc"])
                for error in exc.errors()
            }
        )

    @staticmethod
    def _build_task_error(result: AnalysisResult) -> str | None:
        if result.status in {TaskStatus.DEGRADED, TaskStatus.FAILED, TaskStatus.PARTIAL_SUCCESS}:
            return result.fallback.reason
        return None

    @staticmethod
    def _sanitize_responses(items: Any) -> list[dict[str, Any]]:
        if not isinstance(items, list):
            return []

        sanitized: list[dict[str, Any]] = []
        for item in items:
            if not isinstance(item, dict):
                continue
            try:
                sanitized.append(StructuredResponse.model_validate(item).model_dump(mode="python"))
            except ValidationError:
                continue
        return sanitized

    @staticmethod
    def _sanitize_tool_logs(items: Any) -> list[dict[str, Any]]:
        if not isinstance(items, list):
            return []

        sanitized: list[dict[str, Any]] = []
        for item in items:
            if not isinstance(item, dict):
                continue
            try:
                sanitized.append(ToolLog.model_validate(item).model_dump(mode="python"))
            except ValidationError:
                continue
        return sanitized
