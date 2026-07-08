import logging

from pydantic import Field

from pyrannic import Configuration


class LoggingConfig(Configuration):
    level: int = Field(default=logging.DEBUG)
    """The logging level to use for the application.
    This can be set to any of the standard logging levels (e.g., DEBUG, INFO, WARNING, ERROR, CRITICAL)."""

    handlers: list[logging.Handler] = Field(
        default_factory=lambda: [logging.StreamHandler()]
    )
    """A list of logging handlers to use for the application.
    Handlers determine where the log messages are output, such as to the console, a file, or a remote logging server."""

    @property
    def env_prefix(self) -> str:
        return "LOG_"
