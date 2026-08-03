from fastapi import HTTPException, status


class ForbiddenException(HTTPException):
    def __init__(
        self,
        message: str | None = None,
        headers: dict[str, str] | None = None,
    ):
        if not message:
            message = "This action is forbidden."

        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=message,
            headers=headers,
        )
