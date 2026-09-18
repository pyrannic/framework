from typing import Annotated

from pyrannic.bootstrap.service_provider import ServiceProvider
from pyrannic.container.params import Resolves
from pyrannic.contracts import (
    AsyncAuthTypeInterface,
    AuthTypeInterface,
    ConnectionDriverInterface,
    ConnectorInterface,
    DatabaseManagerInterface,
)
from pyrannic.database.auth_types.password import (
    AsyncPasswordAuthType,
    PasswordAuthType,
)
from pyrannic.database.manager import DatabaseManager
from pyrannic.facades import Config

from .connection_driver import ConnectionDriver
from .connector import AsyncConnector, Connector


class DatabaseServiceProvider(ServiceProvider):
    @property
    def is_critical(self) -> bool:
        return True

    @property
    def connector(self) -> type[ConnectorInterface]:
        default_driver = Config.str("orm.default")
        is_asyncio = Config.bool(f"orm.drivers.{default_driver}.asyncio")

        return AsyncConnector if is_asyncio else Connector

    def register(self):
        self.container.scoped_if(AuthTypeInterface, PasswordAuthType)
        self.container.scoped_if(AsyncAuthTypeInterface, AsyncPasswordAuthType)
        self.container.scoped_if(ConnectionDriverInterface, ConnectionDriver)
        self.container.scoped_if(DatabaseManagerInterface, DatabaseManager)
        self.container.scoped_if(ConnectorInterface, self.connector)

    async def boot(self, manager: Annotated[DatabaseManagerInterface, Resolves()]):
        await manager.migrate()

    async def shutdown(self, manager: Annotated[DatabaseManagerInterface, Resolves()]):
        await manager.disconnect()
