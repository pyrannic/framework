from abc import ABC, abstractmethod
from collections.abc import Callable
from typing import Any, Self, Sequence

from .authorizable import AuthorizableInterface


class GateInterface(ABC):
    @abstractmethod
    def has(self, *abilities: str) -> bool:
        """
        Determine if a given ability has been defined.

        :param abilities: The ability/abilities to check.
        :return: True if the ability is / abilities are defined, False otherwise.
        """

    @abstractmethod
    async def allows(
        self,
        abilities: str | Sequence[str],
        *args: Any,
        **kwargs: Any,
    ) -> bool:
        """
        Determine if all of the given abilities should be granted for the current user.

        :param abilities: The abilities to check.
        :param args: Additional positional arguments.
        :param kwargs: Additional keyword arguments.
        """

    @abstractmethod
    async def check(
        self,
        abilities: str | Sequence[str],
        *args: Any,
        **kwargs: Any,
    ) -> bool:
        """
        Determine if all of the given abilities should be granted for the current user.

        :param abilities: The abilities to check.
        :param args: Additional positional arguments.
        :param kwargs: Additional keyword arguments.
        """

    @abstractmethod
    async def denies(
        self,
        abilities: str | Sequence[str],
        *args: Any,
        **kwargs: Any,
    ) -> bool:
        """
        Determine if any of the given abilities should be denied for the current user.

        :param abilities: The abilities to check.
        :param args: Additional positional arguments.
        :param kwargs: Additional keyword arguments.
        """

    @abstractmethod
    async def any(
        self,
        abilities: str | Sequence[str],
        *args: Any,
        **kwargs: Any,
    ) -> bool:
        """
        Determine if any one of the given abilities should be granted for the current user.

        :param abilities: The abilities to check.
        :param args: Additional positional arguments.
        :param kwargs: Additional keyword arguments.
        """

    @abstractmethod
    async def none(
        self,
        abilities: str | Sequence[str],
        *args: Any,
        **kwargs: Any,
    ) -> bool:
        """
        Determine if none of the given abilities should be granted for the current user.

        :param abilities: The abilities to check.
        :param args: Additional positional arguments.
        :param kwargs: Additional keyword arguments.
        """

    @abstractmethod
    def authorize(
        self,
        ability: str,
        *args: Any,
        **kwargs: Any,
    ) -> Any:
        """
        Determine if the given ability should be granted for the current user.

        :param ability: The ability to check.
        :param args: Additional positional arguments.
        :param kwargs: Additional keyword arguments.

        :raises AuthorizationException: If the user is not authorized.
        """

    @abstractmethod
    def for_user(self, user: AuthorizableInterface) -> Self:
        """
        Get a guard instance for the given user.

        :param user: The user to get the gate instance for.
        :return: A new gate instance for the specified user.
        """

    @abstractmethod
    def set_user(self, user: AuthorizableInterface | None) -> Self:
        """
        Set the user for the current gate instance.

        :param user: The user to set.
        :return: The current gate instance.
        """

    @property
    @abstractmethod
    def user(self) -> AuthorizableInterface:
        """
        Get the current user to check authorization for.

        :return: The current user.
        """

    @abstractmethod
    def define_ability(self, ability: str, callback: Callable[..., bool]) -> Self:
        """
        Define a new ability.

        :param ability: The name of the ability.
        :param callback: A callback that determines if the ability is granted.
        :return: The current gate instance.
        """

    @abstractmethod
    def define_policy(self, model: type[Any], policy: type[Any]) -> Self:
        """
        Register a policy for a given model.

        :param model: The model class to register the policy for.
        :param policy: The policy class to register.
        :return: The current gate instance.
        """

    @abstractmethod
    def guess_policy_names_using(
        self,
        callback: Callable[[str], str | list[str]],
    ) -> Self:
        """
        Set a callback to guess policy names for resources.
        The names must contain the full module path and class name of the policy.
        E.g.: "myapp.policies.foo.FooPolicy" or ["myapp.policies.foo.FooPolicy", "myapp.policies.bar.BarPolicy"].

        :param callback: A callback that takes a resource name and returns a policy name or a list of policy names.
        :return: The current gate instance.
        """
