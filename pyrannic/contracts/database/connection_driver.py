from abc import ABC, abstractmethod
from collections.abc import Callable
from types import CoroutineType
from typing import Any

from sqlalchemy.engine.interfaces import DBAPIConnection


class ConnectionDriverInterface(ABC):
    @property
    @abstractmethod
    def url(self) -> str:
        """
        Returns the URL for the database connection.
        """

    @abstractmethod
    async def disconnect(self) -> None:
        """
        Closes and disposes any connection resource.
        """

    @property
    @abstractmethod
    def factory(
        self,
    ) -> (
        Callable[..., DBAPIConnection | CoroutineType[Any, Any, DBAPIConnection]] | None
    ):
        """
        Returns a callable that creates a new database connection, or None if not applicable.
        """
