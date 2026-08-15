from abc import ABC, abstractmethod
from typing import Any, Generic, Self

from .authenticatable import AuthenticatableType


class GuardInterface(ABC, Generic[AuthenticatableType]):
    @property
    @abstractmethod
    def check(self) -> bool:
        """
        Determine if the current user is authenticated.

        :return: True if the user is authenticated, False otherwise.
        """

    @property
    @abstractmethod
    def is_guest(self) -> bool:
        """
        Determine if the current user is a guest.

        :return: True if the user is a guest, False otherwise.
        """

    @property
    @abstractmethod
    def user(self) -> AuthenticatableType:
        """
        Get the currently authenticated user.

        :return: The authenticated user.
        """

    @property
    @abstractmethod
    def maybe_user(self) -> AuthenticatableType | None:
        """
        Get the currently authenticated user.

        :return: The authenticated user or None if not authenticated.
        """

    @property
    @abstractmethod
    def id(self) -> str | None:
        """
        Get the ID of the currently authenticated user.

        :return: The user ID.
        """

    @property
    @abstractmethod
    def maybe_id(self) -> str | None:
        """
        Get the ID of the currently authenticated user.

        :return: The user ID or None if not authenticated.
        """

    @abstractmethod
    def validate(self, *args: Any, **kwargs: Any) -> bool:
        """
        Validate a user's credentials.

        :param args: Positional arguments for the credentials.
        :param kwargs: Keyword arguments for the credentials.
        :return: True if the credentials are valid, False otherwise.
        """

    @property
    @abstractmethod
    def has_user(self) -> bool:
        """
        Determine if the guard has a user instance.

        :return: True if there is an authenticated user, False otherwise.
        """

    @abstractmethod
    def set_user(self, user: AuthenticatableType) -> Self:
        """
        Set the current user.

        :param user: An instance of AuthenticatableInterface representing the user.
        """
