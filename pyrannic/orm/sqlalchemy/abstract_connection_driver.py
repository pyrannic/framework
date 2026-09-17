from collections.abc import Callable, Coroutine
from typing import Any

from sqlalchemy import URL
from sqlalchemy.engine.interfaces import DBAPIConnection

from pyrannic.contracts import (
    AsyncAuthTypeInterface,
    AuthTypeInterface,
    ConfigRepositoryInterface,
    ConnectionDriverInterface,
)


class AbstractConnectionDriver(ConnectionDriverInterface):
    _url: str | None = None
    _config: ConfigRepositoryInterface
    _auth_type: AsyncAuthTypeInterface | AuthTypeInterface

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
    ) -> Callable[..., DBAPIConnection | Coroutine[Any, Any, DBAPIConnection]] | None:
        return None
