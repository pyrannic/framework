from abc import ABC, abstractmethod
from typing import Any


class AuthTypeInterface(ABC):
    @property
    @abstractmethod
    def password(self) -> str | Any | None:
        """
        Returns the password for the database connection.
        """

    @abstractmethod
    def close(self) -> Any:
        """
        Closes any resources associated with the authentication type.
        """
