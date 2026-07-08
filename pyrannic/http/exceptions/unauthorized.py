from fastapi import status, HTTPException


class UnauthorizedException(HTTPException):
    def __init__(
        self,
        message: str = "Unauthorized",
        headers: dict[str, str] | None = None,
    ):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=message,
            headers=headers,
        )
