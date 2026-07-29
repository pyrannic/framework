from fastapi import HTTPException, status


class ForbiddenException(HTTPException):
    def __init__(
        self,
        message: str = "This action is forbidden.",
        headers: dict[str, str] | None = None,
    ):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=message,
            headers=headers,
        )
