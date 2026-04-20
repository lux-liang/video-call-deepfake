from __future__ import annotations

from fastapi import APIRouter

from app.api.routes.analysis import router as analysis_router
from app.api.routes.demo import router as demo_router
from app.api.routes.health import router as health_router


api_router = APIRouter()
api_router.include_router(health_router)
api_router.include_router(demo_router)
api_router.include_router(analysis_router)
