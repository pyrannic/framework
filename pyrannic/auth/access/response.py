from typing import Any, Self

from pyrannic.auth.forbidden_exception import ForbiddenException


class Response:
    _allowed: bool
    """Indicates whether the response of an authorization was allowed."""

    _message: str | None
    """The message associated with the response of an authorization."""

    _code: Any
    """The code associated with the response of an authorization."""

    _status: int | None
    """The HTTP response status code associated with the response of an authorization."""

    def __init__(
        self,
        allowed: bool,
        message: str | None = None,
        code: Any = None,
    ) -> None:
        self._allowed = allowed
        self._message = message
        self._code = code

    @property
    def allowed(self) -> bool:
        """Determine if the response was allowed."""
        return self._allowed

    @property
    def denied(self) -> bool:
        """Determine if the response was denied."""
        return not self._allowed

    @property
    def message(self) -> str | None:
        """Get the response message."""
        return self._message

    @property
    def code(self) -> Any:
        """Get the response code."""
        return self._code

    @property
    def status(self) -> int | None:
        """Get the HTTP response status code."""
        return self._status

    def with_status(self, status: int) -> Self:
        """Set the HTTP response status code."""
        self._status = status
        return self

    @classmethod
    def allow(cls, message: str | None = None, code: Any = None) -> Self:
        """Create a new "allow" Response."""
        return cls(True, message, code)

    @classmethod
    def deny(cls, message: str | None = None, code: Any = None) -> Self:
        """Create a new "deny" Response."""
        return cls(False, message, code)

    def authorize(self) -> Self:
        """Authorize the response, raising an exception if denied."""
        if self.denied:
            raise ForbiddenException(message=self.message)

        return self
