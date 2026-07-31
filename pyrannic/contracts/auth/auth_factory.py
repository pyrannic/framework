from abc import ABC, abstractmethod

from .guard import GuardInterface


class AuthFactory(ABC):
    @abstractmethod
    def guard(self, name: str) -> GuardInterface:
        """
        Get a guard instance by name.

        :param name: The name of the guard to get.
        :return: An instance of the specified guard.
        """
