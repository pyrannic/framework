from collections.abc import Callable
from types import CoroutineType
from typing import Any

from sqlalchemy import URL
from sqlalchemy.engine.interfaces import DBAPIConnection

from pyrannic.contracts import (
    AuthTypeInterface,
    ConfigRepositoryInterface,
    ConnectionDriverInterface,
)
from pyrannic.ioc import Resolves


class ConnectionDriver(ConnectionDriverInterface):
    _url: str | None = None

    def __init__(
        self,
        auth_type: Resolves[AuthTypeInterface],
        config: Resolves[ConfigRepositoryInterface],
    ):
        self._auth_type = auth_type
        self._config = config

    async def __ioc_call__(self):
        fecther = self.auth_type.fetch_password()

        if fecther is not None:
            await fecther

        self._url = None

    def disconnect(self) -> CoroutineType[Any, Any, None] | None:
        return self._auth_type.close()

    @property
    def auth_type(self) -> AuthTypeInterface:
        return self._auth_type

    @property
    def url(self) -> str:
        if not self._url:
            connection = self._config.string("database.connection", default="sqlite")
            url = self._config.optional_str(f"database.connections.{connection}.url")

            if url:
                self._url = url
            else:
                self._url = (
                    URL
                    .create(
                        drivername=self._config.string(
                            f"database.connections.{connection}.driver"
                        ),
                        username=self._config.optional_str(
                            f"database.connections.{connection}.username"
                        ),
                        password=self._auth_type.password,
                        host=self._config.optional_str(
                            f"database.connections.{connection}.host"
                        ),
                        port=self._config.optional_int(
                            f"database.connections.{connection}.port"
                        ),
                        database=self._config.optional_str(
                            f"database.connections.{connection}.database"
                        ),
                        query=self._config.dict(
                            f"database.connections.{connection}.query"
                        ),
                    )
                    .render_as_string(hide_password=False)
                    .replace("%40", "@")
                )

        return self._url

    @property
    def factory(
        self,
    ) -> (
        Callable[..., DBAPIConnection | CoroutineType[Any, Any, DBAPIConnection]] | None
    ):
        return None
