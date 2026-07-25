import pytest_asyncio

from pyrannic.contracts import (
    ApplicationInterface,
    ConnectorInterface,
    DatabaseManagerInterface,
    RepositoryInterface,
)
from pyrannic.database.manager import DatabaseManager
from pyrannic.facades import Config
from pyrannic.orm.sqlalchemy import Connector, Repository
from tests.unit.orm.sqlalchemy.utils import BarModel


@pytest_asyncio.fixture()
async def repository(
    application: ApplicationInterface,
) -> RepositoryInterface[BarModel]:
    Config.set("database.connections.sqlite.database", ":memory:")

    application.container.singleton(ConnectorInterface, Connector)
    application.container.singleton(DatabaseManagerInterface, DatabaseManager)

    return await application.container.make(Repository[BarModel])
