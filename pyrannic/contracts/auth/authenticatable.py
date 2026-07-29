from abc import ABC, abstractmethod


class AuthenticatableInterface(ABC):
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

    @abstractmethod
    def get_remember_token(self) -> str:
        """
        Get the token value for the "remember me" session.

        :return: The token value.
        """

    @abstractmethod
    def set_remember_token(self, value: str) -> None:
        """
        Set the token value for the "remember me" session.

        :param value: The token value.
        """

    @abstractmethod
    def get_remember_token_name(self) -> str:
        """
        Get the column name for the "remember me" token.

        :return: The column name.
        """
