from __future__ import annotations

from datetime import datetime, timezone
from threading import Lock
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field

from app.core.errors import AppError
from app.schemas.analysis import AnalysisResult, AnalyzeMode, TaskStatus, UploadRequest


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


class UploadRecord(BaseModel):
    model_config = ConfigDict(extra="forbid")

    upload_id: str
    task_id: str
    meeting_id: str
    filename: str
    content_type: str
    source: str
    created_at: datetime = Field(default_factory=utcnow)


class TaskRecord(BaseModel):
    model_config = ConfigDict(extra="forbid")

    task_id: str
    upload_id: str
    meeting_id: str
    requested_mode: str = AnalyzeMode.PLAYBACK_MOCK.value
    use_mock: bool = True
    status: TaskStatus = TaskStatus.QUEUED
    progress: int = 0
    stage: str = "uploaded"
    confidence: float = 0.0
    error: str | None = None
    result: AnalysisResult | None = None
    report_markdown: str | None = None
    created_at: datetime = Field(default_factory=utcnow)
    updated_at: datetime = Field(default_factory=utcnow)


class TaskStore:
    def __init__(self) -> None:
        self._lock = Lock()
        self._uploads: dict[str, UploadRecord] = {}
        self._tasks: dict[str, TaskRecord] = {}

    def create_upload(self, payload: UploadRequest) -> tuple[UploadRecord, TaskRecord]:
        upload_id = self._build_id("upload")
        task_id = self._build_id("task")
        meeting_id = self._build_id("meeting")

        upload = UploadRecord(
            upload_id=upload_id,
            task_id=task_id,
            meeting_id=meeting_id,
            filename=payload.filename,
            content_type=payload.content_type,
            source=payload.source.value,
        )
        task = TaskRecord(
            task_id=task_id,
            upload_id=upload_id,
            meeting_id=meeting_id,
        )

        with self._lock:
            self._uploads[upload_id] = upload
            self._tasks[task_id] = task

        return upload.model_copy(deep=True), task.model_copy(deep=True)

    def get_upload(self, upload_id: str) -> UploadRecord:
        with self._lock:
            upload = self._uploads.get(upload_id)
        if upload is None:
            raise AppError(
                status_code=404,
                code="upload_not_found",
                message=f"upload '{upload_id}' was not found",
            )
        return upload.model_copy(deep=True)

    def get_task(self, task_id: str) -> TaskRecord:
        with self._lock:
            task = self._tasks.get(task_id)
        if task is None:
            raise AppError(
                status_code=404,
                code="task_not_found",
                message=f"task '{task_id}' was not found",
            )
        return task.model_copy(deep=True)

    def update_task(self, task_id: str, **changes: object) -> TaskRecord:
        with self._lock:
            task = self._tasks.get(task_id)
            if task is None:
                raise AppError(
                    status_code=404,
                    code="task_not_found",
                    message=f"task '{task_id}' was not found",
                )

            updated = task.model_copy(deep=True)
            for field, value in changes.items():
                setattr(updated, field, value)
            updated.updated_at = utcnow()
            self._tasks[task_id] = updated

        return updated.model_copy(deep=True)

    @staticmethod
    def _build_id(prefix: str) -> str:
        return f"{prefix}_{uuid4().hex[:10]}"
