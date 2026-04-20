from __future__ import annotations

import logging
from typing import Any

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.schemas.analysis import APIError, ErrorField, ErrorResponse


logger = logging.getLogger(__name__)


class AppError(Exception):
    def __init__(
        self,
        *,
        status_code: int,
        code: str,
        message: str,
        details: list[ErrorField] | dict[str, Any] | None = None,
    ) -> None:
        self.status_code = status_code
        self.code = code
        self.message = message
        self.details = details
        super().__init__(message)


def _error_response(
    *,
    status_code: int,
    code: str,
    message: str,
    details: list[ErrorField] | dict[str, Any] | None = None,
) -> JSONResponse:
    payload = ErrorResponse(
        error=APIError(code=code, message=message, details=details),
    )
    return JSONResponse(
        status_code=status_code,
        content=payload.model_dump(mode="json"),
    )


async def app_error_handler(_: Request, exc: AppError) -> JSONResponse:
    return _error_response(
        status_code=exc.status_code,
        code=exc.code,
        message=exc.message,
        details=exc.details,
    )


async def request_validation_error_handler(_: Request, exc: RequestValidationError) -> JSONResponse:
    details = [
        ErrorField(
            field=".".join(str(part) for part in error["loc"] if part != "body"),
            message=error["msg"],
        )
        for error in exc.errors()
    ]
    return _error_response(
        status_code=422,
        code="request_validation_error",
        message="request validation failed",
        details=details,
    )


async def http_exception_handler(_: Request, exc: HTTPException) -> JSONResponse:
    detail = exc.detail if isinstance(exc.detail, str) else "request failed"
    return _error_response(
        status_code=exc.status_code,
        code="http_error",
        message=detail,
    )


async def unhandled_exception_handler(_: Request, exc: Exception) -> JSONResponse:
    logger.exception("Unhandled backend exception", exc_info=exc)
    return _error_response(
        status_code=500,
        code="internal_error",
        message="internal server error",
    )


def register_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(AppError, app_error_handler)
    app.add_exception_handler(RequestValidationError, request_validation_error_handler)
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(Exception, unhandled_exception_handler)
