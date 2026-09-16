from typing import Any

from pyrannic.contracts import ConfigRepositoryInterface
from pyrannic.contracts.database import AuthTypeInterface
from pyrannic.ioc import Resolves


class PasswordAuthType(AuthTypeInterface):
    def __init__(self, config: Resolves[ConfigRepositoryInterface]):
        self._config = config

    @property
    def password(self) -> str | Any | None:
        connection = self._config.string("database.connection", default="sqlite")
        return self._config.optional_str(f"database.connections.{connection}.password")
