from __future__ import annotations

from fastapi import APIRouter, Depends

from app.api.deps import get_analysis_service
from app.schemas.analysis import (
    AnalysisResult,
    AnalyzeRequest,
    AnalyzeResponse,
    ReportResponse,
    TaskStatusResponse,
    UploadRequest,
    UploadResponse,
)
from app.services.analysis_service import AnalysisService


router = APIRouter(tags=["analysis"])


@router.post("/api/upload", response_model=UploadResponse)
def upload_video(
    payload: UploadRequest,
    service: AnalysisService = Depends(get_analysis_service),
) -> UploadResponse:
    return service.create_upload(payload)


@router.post("/api/analyze", response_model=AnalyzeResponse)
def analyze_video(
    payload: AnalyzeRequest,
    service: AnalysisService = Depends(get_analysis_service),
) -> AnalyzeResponse:
    return service.start_analysis(payload)


@router.get("/api/task/{task_id}", response_model=TaskStatusResponse)
def get_task(
    task_id: str,
    service: AnalysisService = Depends(get_analysis_service),
) -> TaskStatusResponse:
    return service.get_task_status(task_id)


@router.get("/api/result/{task_id}", response_model=AnalysisResult)
def get_result(
    task_id: str,
    service: AnalysisService = Depends(get_analysis_service),
) -> AnalysisResult:
    return service.get_result(task_id)


@router.get("/api/report/{task_id}", response_model=ReportResponse)
def get_report(
    task_id: str,
    service: AnalysisService = Depends(get_analysis_service),
) -> ReportResponse:
    return service.get_report(task_id)
