import os

from typing_extensions import Annotated

from pyrannic.container.params import Resolves
from pyrannic.contracts.application import ApplicationInterface
from pyrannic.contracts.database.connector import ConnectorInterface
from pyrannic.contracts.database.migration import MigrationInterface
from pyrannic.support.path import get_module_paths
from pyrannic.support.reflection import get_classes


class DatabaseManager(ConnectorInterface):
    def __init__(
        self,
        application: Annotated[ApplicationInterface, Resolves()],
        connector: Annotated[ConnectorInterface, Resolves()],
    ) -> None:
        self._application = application
        self._connector = connector

    @property
    def connection(self):
        return self._connector.connection

    async def disconnect(self) -> None:
        await self._connector.disconnect()

    async def migrate(
        self,
        migrations: list[type[MigrationInterface]] | None = None,
    ) -> None:
        if migrations is None:
            modules = get_module_paths(
                os.path.join(self._application.base_path, "database/migrations/tables")
            )
            migrations = get_classes(modules, class_suffix="Table")

        await self._connector.migrate(migrations)
