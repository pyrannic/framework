from typing import cast

from pyrannic.contracts import (
    AuthTypeInterface,
    ConfigRepositoryInterface,
)
from pyrannic.ioc import Resolves
from pyrannic.orm.sqlalchemy.abstract_connection_driver import AbstractConnectionDriver


class ConnectionDriver(AbstractConnectionDriver):
    def __init__(
        self,
        auth_type: Resolves[AuthTypeInterface],
        config: Resolves[ConfigRepositoryInterface],
    ):
        self._auth_type = auth_type
        self._config = config

    async def __ioc_call__(self):
        self._auth_type.fetch_password()
        self._url = None

    async def disconnect(self) -> None:
        self._auth_type.close()

    @property
    def auth_type(self) -> AuthTypeInterface:
        return cast(AuthTypeInterface, self._auth_type)
