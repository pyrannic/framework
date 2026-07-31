from abc import ABC, abstractmethod
from typing import Any

from .authenticatable import AuthenticatableInterface


class UserProviderInterface(ABC):
    @abstractmethod
    async def retrieve_by_id(self, identifier: Any) -> AuthenticatableInterface | None:
        """
        Retrieve a user by their unique identifier.

        :param identifier: The unique identifier of the user.
        :return: The user object or None if not found.
        """

    @abstractmethod
    async def retrieve_by_token(
        self,
        identifier: Any,
        token: str,
    ) -> AuthenticatableInterface | None:
        """
        Retrieve a user by their unique identifier and "remember me" token.

        :param identifier: The unique identifier of the user.
        :param token: The "remember me" token.
        :return: The user object or None if not found.
        """

    @abstractmethod
    async def retrieve_by_credentials(
        self,
        credentials: dict[str, Any],
    ) -> AuthenticatableInterface | None:
        """
        Retrieve a user by their credentials.

        :param credentials: The user's credentials.
        :return: The user object or None if not found.
        """

    @abstractmethod
    async def update_remember_token(
        self, user: AuthenticatableInterface, token: str
    ) -> None:
        """
        Update the "remember me" token for the given user in storage.

        :param user: The user object.
        :param token: The new "remember me" token.
        """

    @abstractmethod
    def validate_credentials(
        self,
        user: AuthenticatableInterface,
        credentials: dict[str, Any],
    ) -> bool:
        """
        Validate a user against the given credentials.

        :param user: The user object.
        :param credentials: The user's credentials.
        :return: True if the credentials are valid, False otherwise.
        """
