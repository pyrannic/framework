from fastapi import HTTPException, status


class UnauthorizedException(HTTPException):
    def __init__(
        self,
        message: str | None = None,
        headers: dict[str, str] | None = None,
    ):
        if message is None:
            message = "This action is unauthorized."

        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=message,
            headers=headers,
        )
