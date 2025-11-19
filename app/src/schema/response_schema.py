from pydantic import BaseModel
from typing import Any, Optional
from http import HTTPStatus
from fastapi import status as fastapi_status


class ApiResponse(BaseModel):
    data: Optional[Any] = None
    message: str
    statusCode: int
    status: str

    @staticmethod
    def success(
        data: Any,
        message: str = "Success",
        status_code: int = fastapi_status.HTTP_200_OK,
    ):
        return ApiResponse(
            data=data,
            message=message,
            statusCode=status_code,
            status=HTTPStatus(status_code).phrase,
        )

    @staticmethod
    def error(
        data: Any = None,
        message: str = "Error",
        status_code: int = fastapi_status.HTTP_400_BAD_REQUEST,
    ):
        return ApiResponse(
            data=data,
            message=message,
            statusCode=status_code,
            status=HTTPStatus(status_code).phrase,
        )
