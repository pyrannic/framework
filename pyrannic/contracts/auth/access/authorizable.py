from abc import abstractmethod
from typing import Any


class AuthorizableInterface:
    """
    Interface for authorizable entities.
    """

    @abstractmethod
    async def can(self, abilities: str | list[str], *args: Any, **kwargs: Any) -> bool:
        """
        Determine if the entity has the given abilities.

        :param abilities: The abilities to be authorized.
        :param args: Additional positional arguments.
        :param kwargs: Additional keyword arguments.
        :return: True if authorized, False otherwise.
        """

    @abstractmethod
    async def can_any(
        self,
        abilities: str | list[str],
        *args: Any,
        **kwargs: Any,
    ) -> bool:
        """
        Determine if the entity has any of the given abilities.

        :param abilities: The abilities to be authorized.
        :param args: Additional positional arguments.
        :param kwargs: Additional keyword arguments.
        :return: True if authorized for any ability, False otherwise.
        """

    @abstractmethod
    async def cant(self, abilities: str | list[str], *args: Any, **kwargs: Any) -> bool:
        """
        Determine if the entity does not have the given abilities.

        :param abilities: The abilities to be authorized.
        :param args: Additional positional arguments.
        :param kwargs: Additional keyword arguments.
        :return: True if not authorized, False otherwise.
        """

    @abstractmethod
    async def cannot(
        self,
        abilities: str | list[str],
        *args: Any,
        **kwargs: Any,
    ) -> bool:
        """
        Determine if the entity does not have the given abilities.

        :param abilities: The abilities to be authorized.
        :param args: Additional positional arguments.
        :param kwargs: Additional keyword arguments.
        :return: True if not authorized, False otherwise.
        """
