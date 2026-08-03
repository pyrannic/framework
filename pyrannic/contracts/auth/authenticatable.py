from abc import abstractmethod
from typing import TypeVar


class AuthenticatableInterface:
    """
    Interface for authenticatable users.
    """

    @abstractmethod
    def get_auth_identifier_name(self) -> str:
        """
        Get the name of the unique identifier for the user.

        :return: The name of the unique identifier.
        """

    @abstractmethod
    def get_auth_identifier(self) -> str:
        """
        Get the unique identifier for the user.

        :return: The unique identifier.
        """

    @abstractmethod
    def get_auth_password_name(self) -> str:
        """
        Get the name of the password attribute for the user.

        :return: The name of the password attribute.
        """

    @abstractmethod
    def get_auth_password(self) -> str:
        """
        Get the password for the user.

        :return: The password.
        """


AuthenticatableType = TypeVar("AuthenticatableType", bound=AuthenticatableInterface)
