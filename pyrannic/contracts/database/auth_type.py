from abc import ABC, abstractmethod
from types import CoroutineType
from typing import Any


class AuthTypeInterface(ABC):
    @property
    @abstractmethod
    def password(self) -> str | None:
        """
        Returns the password for the database connection.
        """

    @abstractmethod
    def fetch_password(self) -> CoroutineType[Any, Any, None] | None:
        """
        Fetches the password for the database connection.
        """

    @abstractmethod
    def close(self) -> CoroutineType[Any, Any, None] | None:
        """
        Closes any resources associated with the authentication type.
        """
