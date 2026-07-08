from typing import Annotated

from pyrannic.bootstrap.service_provider import ServiceProvider
from pyrannic.container.params import Resolves
from pyrannic.contracts.database.connector import ConnectorInterface
from pyrannic.contracts.database.manager import DatabaseManagerInterface
from pyrannic.database.manager import DatabaseManager
from pyrannic.orm.sqlalchemy.connector import SqlAlchemyConnector


class DatabaseServiceProvider(ServiceProvider):
    __singletons__ = {
        ConnectorInterface: SqlAlchemyConnector,
        DatabaseManagerInterface: DatabaseManager,
    }

    async def boot(self, manager: Annotated[DatabaseManagerInterface, Resolves()]):
        await manager.migrate()

    async def shutdown(self, manager: Annotated[DatabaseManagerInterface, Resolves()]):
        await manager.disconnect()
