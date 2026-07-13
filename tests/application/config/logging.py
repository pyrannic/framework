import logging

from pydantic import Field

from pyrannic import Configuration


class LoggingConfig(Configuration):
    name: str = Field(default="uvicorn.error")
    """
    The name of the logger to use for the application.
    This can be set to any string value, and it will be used to create a logger instance with that name.
    By default, it is set to "uvicorn.error", which is the default logger name used by Uvicorn.
    """

    level: int = Field(default=logging.DEBUG)
    """The logging level to use for the application.
    This can be set to any of the standard logging levels (e.g., DEBUG, INFO, WARNING, ERROR, CRITICAL)."""

    handlers: list[logging.Handler] = Field(default=[])
    """A list of logging handlers to use for the application.
    Handlers determine where the log messages are output, such as to the console, a file, or a remote logging server."""

    @property
    def env_prefix(self) -> str:
        return "LOG_"
