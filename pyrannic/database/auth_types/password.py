from pyrannic.contracts import ConfigRepositoryInterface
from pyrannic.contracts.database import AuthTypeInterface
from pyrannic.contracts.database.auth_type import AsyncAuthTypeInterface
from pyrannic.ioc import Resolves


class PasswordAuthType(AuthTypeInterface):
    def __init__(self, config: Resolves[ConfigRepositoryInterface]):
        self._config = config
        self._password = None

    @property
    def password(self) -> str | None:
        if not self._password:
            self.fetch_password()

        return self._password

    def fetch_password(self) -> None:
        connection = self._config.string("database.connection", default="sqlite")
        self._password = self._config.optional_str(
            f"database.connections.{connection}.password"
        )

    def close(self) -> None:
        pass


class AsyncPasswordAuthType(AsyncAuthTypeInterface):
    def __init__(self, config: Resolves[ConfigRepositoryInterface]):
        self._config = config
        self._password = None

    @property
    def password(self) -> str | None:
        if not self._password:
            self._fetch_password()

        return self._password

    async def fetch_password(self) -> None:
        self._fetch_password()

    def _fetch_password(self) -> None:
        connection = self._config.string("database.connection", default="sqlite")
        self._password = self._config.optional_str(
            f"database.connections.{connection}.password"
        )

    async def close(self) -> None:
        pass
