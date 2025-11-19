from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from http import HTTPStatus

from app.src.schema.response_schema import ApiResponse


async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content=ApiResponse.error(
            message=exc.detail,
            status_code=exc.status_code,
        ).model_dump(),
    )


async def all_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content=ApiResponse.error(
            message="Internal server error", status_code=500
        ).model_dump(),
    )
