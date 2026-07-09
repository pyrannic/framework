from logging import Logger
from typing import Annotated, Any
from unittest.mock import Mock

from pyrannic.container.param_functions import Resolves
from pyrannic.contracts.application import ApplicationInterface
from pyrannic.contracts.database.manager import DatabaseManagerInterface
from pyrannic.database.migration import Migration
from pyrannic.database.provider import DatabaseServiceProvider


class MockDatabaseServiceProvider(DatabaseServiceProvider):
    def __init__(self, app: ApplicationInterface, logger: Logger | None = None):
        super().__init__(app, logger)
        self.mock = Mock(spec=self)
        self.mock.container = self.container

    @property
    def is_critical(self) -> bool:
        return False

    def register(self) -> None:
        self.mock.register()
        self.container.instance(self.__class__.__name__, self.mock)
        super().register()

    async def initialize(self) -> None:
        await self.mock.initialize()
        await super().initialize()

    async def boot(
        self, manager: Annotated[DatabaseManagerInterface, Resolves()]
    ) -> None:
        await self.mock.boot(manager)
        await super().boot(manager)

    async def shutdown(
        self, manager: Annotated[DatabaseManagerInterface, Resolves()]
    ) -> Any:
        await self.mock.shutdown(manager)
        await super().shutdown(manager)


class FooTable(Migration):
    async def up(self) -> None:
        await self.schema.create("foo_table")

    async def down(self) -> None:
        await self.schema.drop("foo_table")
