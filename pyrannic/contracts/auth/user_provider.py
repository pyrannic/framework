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
    async def retrieve_by_credentials(
        self,
        *args: Any,
        **kwargs: Any,
    ) -> AuthenticatableInterface | None:
        """
        Retrieve a user by their credentials.

        :param credentials: The user's credentials.
        :return: The user object or None if not found.
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
