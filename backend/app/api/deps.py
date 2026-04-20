from __future__ import annotations

from fastapi import Request

from app.services.analysis_service import AnalysisService


def get_analysis_service(request: Request) -> AnalysisService:
    return request.app.state.analysis_service
