from abc import ABC, abstractmethod


class AuthTypeInterface(ABC):
    @property
    @abstractmethod
    def password(self) -> str | None:
        """
        Returns the password for the database connection.
        """

    @abstractmethod
    def fetch_password(self) -> None:
        """
        Fetches the password for the database connection.
        """

    @abstractmethod
    def close(self) -> None:
        """
        Closes any resources associated with the authentication type.
        """


class AsyncAuthTypeInterface(ABC):
    @property
    @abstractmethod
    def password(self) -> str | None:
        """
        Returns the password for the database connection.
        """

    @abstractmethod
    async def fetch_password(self) -> None:
        """
        Fetches the password for the database connection.
        """

    @abstractmethod
    async def close(self) -> None:
        """
        Closes any resources associated with the authentication type.
        """
