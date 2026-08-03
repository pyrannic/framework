from typing import Any

from pyrannic.contracts.auth import AuthorizableInterface, GateInterface
from pyrannic.facades import App


class Authorizable(AuthorizableInterface):
    """
    Class that provides authorization capabilities to a model.
    """

    @property
    def _gate(self) -> GateInterface:
        return App.container.instance(GateInterface).for_user(self)

    async def can(self, abilities: str | list[str], *args: Any, **kwargs: Any) -> bool:
        return await self._gate.check(abilities, *args, **kwargs)

    async def can_any(
        self,
        abilities: str | list[str],
        *args: Any,
        **kwargs: Any,
    ) -> bool:
        return await self._gate.any(abilities, *args, **kwargs)

    async def cant(self, abilities: str | list[str], *args: Any, **kwargs: Any) -> bool:
        return not await self.can(abilities, *args, **kwargs)

    async def cannot(
        self,
        abilities: str | list[str],
        *args: Any,
        **kwargs: Any,
    ) -> bool:
        return not await self.can(abilities, *args, **kwargs)
