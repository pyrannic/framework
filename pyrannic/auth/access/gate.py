from abc import abstractmethod
from typing import Any

from pyrannic.contracts import GateInterface


class Gate(GateInterface):
    _abilities: dict[str, Any] = {}
    _policies: dict[str, Any] = {}

    def __init__(
        self,
        abilities: dict[str, Any] = {},
        policies: dict[str, Any] = {},
    ) -> None:
        self._abilities = abilities
        self._policies = policies

    @abstractmethod
    def has(self, ability: str | Any) -> bool:
        """
        Determine if a given ability has been defined.

        :param ability: The ability to check.
        :return: True if the ability is defined, False otherwise.
        """

    @abstractmethod
    def allows(self, abilities: str | list[str], *args: Any, **kwargs: Any) -> bool:
        """
        Determine if all of the given abilities should be granted for the current user.

        :param abilities: The abilities to check.
        :param args: Additional positional arguments.
        :param kwargs: Additional keyword arguments.
        """

    @abstractmethod
    def check(self, abilities: str | list[str], *args: Any, **kwargs: Any) -> bool:
        """
        Determine if all of the given abilities should be granted for the current user.

        :param abilities: The abilities to check.
        :param args: Additional positional arguments.
        :param kwargs: Additional keyword arguments.
        """

    @abstractmethod
    def denies(self, abilities: str | list[str], *args: Any, **kwargs: Any) -> bool:
        """
        Determine if any of the given abilities should be denied for the current user.

        :param abilities: The abilities to check.
        :param args: Additional positional arguments.
        :param kwargs: Additional keyword arguments.
        """

    @abstractmethod
    def any(self, abilities: str | list[str], *args: Any, **kwargs: Any) -> bool:
        """
        Determine if any one of the given abilities should be granted for the current user.

        :param abilities: The abilities to check.
        :param args: Additional positional arguments.
        :param kwargs: Additional keyword arguments.
        """

    @abstractmethod
    def authorize(self, abilities: str | list[str], *args: Any, **kwargs: Any) -> bool:
        """
        Determine if the given ability should be granted for the current user.

        :param abilities: The abilities to check.
        :param args: Additional positional arguments.
        :param kwargs: Additional keyword arguments.
        :return: True if the ability is granted, False otherwise.
        :raises AuthorizationException: If the user is not authorized.
        """

    @abstractmethod
    def forUser(self, user: Any) -> "GateInterface":
        """
        Get a guard instance for the given user.

        :param user: The user to get the gate instance for.
        :return: A new gate instance for the specified user.
        """
