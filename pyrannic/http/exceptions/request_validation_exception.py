from typing import Any

from fastapi.exceptions import RequestValidationError


class RequestValidationException(RequestValidationError):
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
                    "msg": message or "field not valid",
                    "type": error_type or "value_error.not_valid",
                }
            ],
            body=id_,
        )
