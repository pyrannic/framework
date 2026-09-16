from typing import cast

from pyrannic.contracts import (
    AsyncAuthTypeInterface,
    ConfigRepositoryInterface,
)
from pyrannic.ioc import Resolves
from pyrannic.orm.sqlalchemy.abstract_connection_driver import AbstractConnectionDriver


class ConnectionDriver(AbstractConnectionDriver):
    def __init__(
        self,
        auth_type: Resolves[AsyncAuthTypeInterface],
        config: Resolves[ConfigRepositoryInterface],
    ):
        self._auth_type = auth_type
        self._config = config

    async def __ioc_call__(self):
        await self.auth_type.fetch_password()
        self._url = None

    async def disconnect(self) -> None:
        await self.auth_type.close()

    @property
    def auth_type(self) -> AsyncAuthTypeInterface:
        return cast(AsyncAuthTypeInterface, self._auth_type)
