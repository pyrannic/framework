from typing import Any, Self

from pyrannic.contracts import AuthorizableInterface, GateInterface


class Gate(GateInterface):
    _user: AuthorizableInterface  # TODO
    _abilities: dict[str, Any] = {}
    _policies: dict[str, Any] = {}

    def __init__(
        self,
        abilities: dict[str, Any] = {},
        policies: dict[str, Any] = {},
    ) -> None:
        self._abilities = abilities
        self._policies = policies

    def has(self, ability: str | Any) -> bool:
        return False

    def allows(self, abilities: str | list[str], *args: Any, **kwargs: Any) -> bool:
        return False

    def check(self, abilities: str | list[str], *args: Any, **kwargs: Any) -> bool:
        return False

    def denies(self, abilities: str | list[str], *args: Any, **kwargs: Any) -> bool:
        return True

    def any(self, abilities: str | list[str], *args: Any, **kwargs: Any) -> bool:
        return False

    def authorize(self, abilities: str | list[str], *args: Any, **kwargs: Any) -> bool:
        # TODO
        raise NotImplementedError("TODO - The 'authorize' method must be implemented.")

    def for_user(self, user: AuthorizableInterface) -> Self:
        self._user = user
        return self
