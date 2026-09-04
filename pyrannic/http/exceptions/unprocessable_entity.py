from typing import Any

from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel
from starlette.responses import JSONResponse

from pyrannic.http.exceptions.exception import HttpExceptionResponse


class UnprocessableEntityException(RequestValidationError):
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
                    "msg": message or "unprocessable entity",
                    "type": error_type or "value_error.unprocessable_entity",
                }
            ],
            body=id_,
        )


class UnprocessableContentResponse(BaseModel):
    detail: list[HttpExceptionResponse]
    resource_id: Any


def handle_unprocessable_entity_exception(
    _: Request,
    exception: Exception,
) -> JSONResponse:
    assert isinstance(exception, UnprocessableEntityException)

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
        content={
            "detail": exception.errors(),
            "resource_id": exception.body,
        },
    )
