from abc import ABC, abstractmethod
from typing import Any


class LoggerInterface(ABC):
    @abstractmethod
    def setLevel(self, level: int | str) -> None:
        """Set the logging level of this logger."""

    @abstractmethod
    def debug(self, msg: str, *args: Any, **kwargs: Any) -> None:
        """
        Log 'msg % args' with severity 'DEBUG'.

        To pass exception information, use the keyword argument exc_info with
        a true value, e.g.

        logger.debug("Houston, we have a %s", "thorny problem", exc_info=True)
        """

    @abstractmethod
    def info(self, msg: str, *args: Any, **kwargs: Any) -> None:
        """
        Log 'msg % args' with severity 'INFO'.

        To pass exception information, use the keyword argument exc_info with
        a true value, e.g.

        logger.info("Houston, we have a %s", "notable problem", exc_info=True)
        """

    @abstractmethod
    def warning(self, msg: str, *args: Any, **kwargs: Any) -> None:
        """
        Log 'msg % args' with severity 'WARNING'.

        To pass exception information, use the keyword argument exc_info with
        a true value, e.g.

        logger.warning("Houston, we have a %s", "bit of a problem", exc_info=True)
        """

    @abstractmethod
    def error(self, msg: str, *args: Any, **kwargs: Any) -> None:
        """
        Log 'msg % args' with severity 'ERROR'.

        To pass exception information, use the keyword argument exc_info with
        a true value, e.g.

        logger.error("Houston, we have a %s", "major problem", exc_info=True)
        """

    @abstractmethod
    def exception(self, msg: str, *args: Any, **kwargs: Any) -> None:
        """
        Convenience method for logging an ERROR with exception information.
        """

    @abstractmethod
    def critical(self, msg: str, *args: Any, **kwargs: Any) -> None:
        """
        Log 'msg % args' with severity 'CRITICAL'.

        To pass exception information, use the keyword argument exc_info with
        a true value, e.g.

        logger.critical("Houston, we have a %s", "major disaster", exc_info=True)
        """

    @abstractmethod
    def log(self, level: int | str, msg: str, *args: Any, **kwargs: Any) -> None:
        """
        Log 'msg % args' with the integer severity 'level'.

        To pass exception information, use the keyword argument exc_info with
        a true value, e.g.

        logger.log(level, "We have a %s", "mysterious problem", exc_info=True)
        """
