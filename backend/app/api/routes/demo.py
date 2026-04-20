from __future__ import annotations

from fastapi import APIRouter, Depends

from app.api.deps import get_analysis_service
from app.schemas.analysis import AnalysisResult
from app.services.analysis_service import AnalysisService


router = APIRouter(tags=["demo"])


@router.get("/api/demo/sample-result", response_model=AnalysisResult)
def get_demo_sample_result(
    service: AnalysisService = Depends(get_analysis_service),
) -> AnalysisResult:
    return service.get_demo_sample_result()
