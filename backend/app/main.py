from __future__ import annotations

from fastapi import FastAPI

from app.schemas.analysis import (
    AnalysisResult,
    AnalyzeRequest,
    AnalyzeResponse,
    ReportResponse,
    TaskStatusResponse,
    UploadRequest,
    UploadResponse,
)
from app.services.sample_data import load_sample_report, load_sample_result


app = FastAPI(
    title="MeetTruth Agent API",
    version="0.1.0",
    description="Phase 1 bootstrap API for video-call deepfake inspection.",
)


@app.get("/healthz")
def healthz() -> dict[str, str]:
    return {"status": "ok", "service": "meettruth-backend"}


@app.post("/api/upload", response_model=UploadResponse)
def upload_video(payload: UploadRequest) -> UploadResponse:
    return UploadResponse(
        task_id="task_demo_001",
        meeting_id="meeting_demo_001",
        upload_id="upload_demo_001",
        status="queued",
        message=f"upload accepted for {payload.filename}",
    )


@app.post("/api/analyze", response_model=AnalyzeResponse)
def analyze_video(payload: AnalyzeRequest) -> AnalyzeResponse:
    return AnalyzeResponse(
        task_id="task_demo_001",
        meeting_id=payload.meeting_id,
        status="processing",
        estimated_mode=payload.mode,
    )


@app.get("/api/task/{task_id}", response_model=TaskStatusResponse)
def get_task(task_id: str) -> TaskStatusResponse:
    return TaskStatusResponse(
        task_id=task_id,
        meeting_id="meeting_demo_001",
        status="completed",
        progress=100,
        stage="reporting",
        confidence=0.78,
        error=None,
    )


@app.get("/api/result/{task_id}", response_model=AnalysisResult)
def get_result(task_id: str) -> AnalysisResult:
    sample = load_sample_result()
    sample["task_id"] = task_id
    sample.pop("task_id", None)
    return AnalysisResult(**sample)


@app.get("/api/demo/sample-result", response_model=AnalysisResult)
def get_demo_sample_result() -> AnalysisResult:
    return AnalysisResult(**load_sample_result())


@app.get("/api/report/{task_id}", response_model=ReportResponse)
def get_report(task_id: str) -> ReportResponse:
    return ReportResponse(
        task_id=task_id,
        meeting_id="meeting_demo_001",
        status="completed",
        report_markdown=load_sample_report(),
        generated_at="2026-04-20T00:00:00Z",
    )
