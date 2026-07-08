from typing import Any

from pydantic import BaseModel
from fastapi import status, Request
from fastapi.exceptions import RequestValidationError
from starlette.responses import JSONResponse

from pyrannic.http.exceptions.exception import HttpExceptionResponse


class ResourceNotFoundException(RequestValidationError):
    def __init__(
        self,
        id_: Any,
        *loc: str,
        loc_type: str = "path",
        error_type: str | None = None,
        message: str | None = None,
    ):
        super().__init__(
            [
                {
                    "loc": (loc_type, *loc),
                    "msg": message or "resource has not been found",
                    "type": error_type or "value_error.resource_not_found",
                }
            ],
            body=id_,
        )


class ResourceNotFoundResponse(BaseModel):
    detail: list[HttpExceptionResponse]
    resource_id: Any


def handle_resource_not_found_exception(
    _: Request,
    exception: Exception,
) -> JSONResponse:
    assert isinstance(exception, ResourceNotFoundException)

    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={
            "detail": exception.errors(),
            "resource_id": exception.body,
        },
    )
