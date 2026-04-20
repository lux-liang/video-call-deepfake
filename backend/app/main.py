from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.router import api_router
from app.core.errors import register_exception_handlers
from app.services.analysis_service import AnalysisService
from app.services.report_service import ReportService
from app.services.task_store import TaskStore


def create_app() -> FastAPI:
    app = FastAPI(
        title="MeetTruth Agent API",
        version="0.2.0",
        description="Phase 1 P0 API for video-call deepfake inspection.",
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=False,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    task_store = TaskStore()
    report_service = ReportService()
    analysis_service = AnalysisService(
        task_store=task_store,
        report_service=report_service,
    )

    app.state.task_store = task_store
    app.state.analysis_service = analysis_service

    register_exception_handlers(app)
    app.include_router(api_router)
    return app


app = create_app()
