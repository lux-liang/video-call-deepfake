from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class UploadRequest(BaseModel):
    filename: str
    content_type: str
    source: str = "local_upload"


class UploadResponse(BaseModel):
    task_id: str
    meeting_id: str
    upload_id: str
    status: str
    message: str


class AnalyzeRequest(BaseModel):
    meeting_id: str
    upload_id: str
    mode: str = "playback_mock"
    use_mock: bool = True


class AnalyzeResponse(BaseModel):
    task_id: str
    meeting_id: str
    status: str
    estimated_mode: str


class TaskStatusResponse(BaseModel):
    task_id: str
    meeting_id: str
    status: str
    progress: int
    stage: str
    confidence: float
    error: str | None = None


class ReportResponse(BaseModel):
    task_id: str
    meeting_id: str
    status: str
    report_markdown: str
    generated_at: str


class AnalysisResult(BaseModel):
    meeting_id: str
    status: str
    confidence: float
    participants: list[dict[str, Any]] = Field(default_factory=list)
    events: list[dict[str, Any]] = Field(default_factory=list)
    responses: list[dict[str, Any]] = Field(default_factory=list)
    risk_scores: list[dict[str, Any]] = Field(default_factory=list)
    suspicious_segments: list[dict[str, Any]] = Field(default_factory=list)
    tool_logs: list[dict[str, Any]] = Field(default_factory=list)
    report_summary: dict[str, Any] = Field(default_factory=dict)
    validation: dict[str, Any] = Field(default_factory=dict)
    fallback: dict[str, Any] = Field(default_factory=dict)
