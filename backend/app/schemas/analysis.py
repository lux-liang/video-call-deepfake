from __future__ import annotations

from datetime import datetime
from enum import StrEnum
from pathlib import Path
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


class TaskStatus(StrEnum):
    QUEUED = "queued"
    PROCESSING = "processing"
    COMPLETED = "completed"
    PARTIAL_SUCCESS = "partial_success"
    DEGRADED = "degraded"
    FAILED = "failed"


class AnalyzeMode(StrEnum):
    PLAYBACK_MOCK = "playback_mock"
    SAMPLE = "sample"
    PIPELINE_REAL = "pipeline_real"


class UploadSource(StrEnum):
    LOCAL_UPLOAD = "local_upload"


class RiskLevel(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class SeverityLevel(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class ToolLogStatus(StrEnum):
    SUCCESS = "success"
    MOCKED = "mocked"
    PARTIAL_SUCCESS = "partial_success"
    DEGRADED = "degraded"
    FAILED = "failed"


ALLOWED_VIDEO_EXTENSIONS = {".avi", ".mkv", ".mov", ".mp4", ".webm"}
ALLOWED_VIDEO_CONTENT_TYPES = {
    "application/octet-stream",
    "video/mp4",
    "video/quicktime",
    "video/webm",
    "video/x-matroska",
    "video/x-msvideo",
}


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class HealthResponse(StrictModel):
    status: Literal["ok"] = "ok"
    service: str
    version: str


class UploadRequest(StrictModel):
    filename: str = Field(min_length=1, max_length=255)
    content_type: str = Field(min_length=1, max_length=128)
    source: UploadSource = UploadSource.LOCAL_UPLOAD

    @field_validator("filename")
    @classmethod
    def validate_filename(cls, value: str) -> str:
        if Path(value).name != value:
            raise ValueError("filename must not contain a path")
        suffix = Path(value).suffix.lower()
        if suffix not in ALLOWED_VIDEO_EXTENSIONS:
            supported = ", ".join(sorted(ALLOWED_VIDEO_EXTENSIONS))
            raise ValueError(f"filename must end with one of: {supported}")
        return value

    @field_validator("content_type")
    @classmethod
    def validate_content_type(cls, value: str) -> str:
        normalized = value.strip().lower()
        if normalized in ALLOWED_VIDEO_CONTENT_TYPES or normalized.startswith("video/"):
            return normalized
        raise ValueError("content_type must be a supported video MIME type")


class UploadResponse(StrictModel):
    task_id: str
    meeting_id: str
    upload_id: str
    status: TaskStatus
    message: str


class AnalyzeRequest(StrictModel):
    meeting_id: str = Field(min_length=1)
    upload_id: str = Field(min_length=1)
    mode: AnalyzeMode = AnalyzeMode.PLAYBACK_MOCK
    use_mock: bool = True

    @model_validator(mode="after")
    def validate_mode_and_mock_flag(self) -> "AnalyzeRequest":
        if self.mode in {AnalyzeMode.PLAYBACK_MOCK, AnalyzeMode.SAMPLE} and not self.use_mock:
            raise ValueError("mock modes require use_mock=true")
        return self


class AnalyzeResponse(StrictModel):
    task_id: str
    meeting_id: str
    status: TaskStatus
    estimated_mode: str


class Participant(StrictModel):
    participant_id: str
    display_name: str
    role: str
    track_ref: str | None = None
    dominant_risk_level: RiskLevel
    notes: str
    metadata: dict[str, Any] = Field(default_factory=dict)


class Event(StrictModel):
    event_id: str
    participant_id: str
    timestamp_start: float = Field(ge=0)
    timestamp_end: float = Field(ge=0)
    event_type: str
    severity: SeverityLevel
    summary: str
    evidence_refs: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_time_range(self) -> "Event":
        if self.timestamp_end < self.timestamp_start:
            raise ValueError("timestamp_end must be greater than or equal to timestamp_start")
        return self


class StructuredResponse(StrictModel):
    response_id: str
    kind: str
    source: str
    summary: str
    confidence: float = Field(ge=0, le=1)


class RiskScore(StrictModel):
    participant_id: str
    score: float = Field(ge=0, le=1)
    level: RiskLevel
    reasons: list[str] = Field(default_factory=list)


class SuspiciousSegment(StrictModel):
    segment_id: str
    timestamp_start: float = Field(ge=0)
    timestamp_end: float = Field(ge=0)
    participant_ids: list[str] = Field(default_factory=list)
    reason: str
    confidence: float = Field(ge=0, le=1)

    @model_validator(mode="after")
    def validate_time_range(self) -> "SuspiciousSegment":
        if self.timestamp_end < self.timestamp_start:
            raise ValueError("timestamp_end must be greater than or equal to timestamp_start")
        return self


class ToolLog(StrictModel):
    tool_name: str
    status: ToolLogStatus
    started_at: datetime
    ended_at: datetime
    summary: str
    artifacts: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_time_range(self) -> "ToolLog":
        if self.ended_at < self.started_at:
            raise ValueError("ended_at must be greater than or equal to started_at")
        return self


class ReportSummary(StrictModel):
    headline: str
    overview: str
    recommended_actions: list[str] = Field(default_factory=list)


class ValidationInfo(StrictModel):
    schema_valid: bool = True
    missing_fields: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    validator_version: str = "phase1-p0"


class FallbackInfo(StrictModel):
    mode: str
    reason: str
    degraded_fields: list[str] = Field(default_factory=list)
    used_sample: bool = False


class AnalysisResult(StrictModel):
    meeting_id: str
    status: TaskStatus
    confidence: float = Field(ge=0, le=1)
    participants: list[Participant] = Field(default_factory=list)
    events: list[Event] = Field(default_factory=list)
    responses: list[StructuredResponse] = Field(default_factory=list)
    risk_scores: list[RiskScore] = Field(default_factory=list)
    suspicious_segments: list[SuspiciousSegment] = Field(default_factory=list)
    tool_logs: list[ToolLog] = Field(default_factory=list)
    report_summary: ReportSummary
    validation: ValidationInfo
    fallback: FallbackInfo


class TaskStatusResponse(StrictModel):
    task_id: str
    meeting_id: str
    status: TaskStatus
    progress: int = Field(ge=0, le=100)
    stage: str
    confidence: float = Field(ge=0, le=1)
    error: str | None = None


class ReportResponse(StrictModel):
    task_id: str
    meeting_id: str
    status: TaskStatus
    report_markdown: str
    generated_at: datetime


class ErrorField(StrictModel):
    field: str
    message: str


class APIError(StrictModel):
    code: str
    message: str
    details: list[ErrorField] | dict[str, Any] | None = None


class ErrorResponse(StrictModel):
    status: Literal["failed"] = "failed"
    error: APIError
