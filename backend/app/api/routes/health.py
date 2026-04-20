from __future__ import annotations

from fastapi import APIRouter

from app.schemas.analysis import HealthResponse


router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthResponse)
@router.get("/healthz", response_model=HealthResponse, include_in_schema=False)
def health() -> HealthResponse:
    return HealthResponse(
        service="meettruth-backend",
        version="0.2.0",
    )
