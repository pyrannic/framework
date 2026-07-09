import pytest
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession

from pyrannic import Config
from pyrannic.contracts.application import ApplicationInterface
from pyrannic.contracts.database.connector import ConnectorInterface
from pyrannic.contracts.database.manager import DatabaseManagerInterface
from pyrannic.database.manager import DatabaseManager
from pyrannic.orm.sqlalchemy import (
    Repository,
    AsyncRepository,
    SqlAlchemyAsyncConnector,
)

from tests.unit.orm.sqlalchemy.utils import BarModel


@pytest.mark.asyncio
async def test_query_builder(application: ApplicationInterface):
    repository = await application.container.resolve(Repository[BarModel])

    assert isinstance(repository.session, Session)


@pytest.mark.asyncio
async def test_async_query_builder(application: ApplicationInterface):
    Config.set("database.connections.sqlite.driver", "sqlite+aiosqlite")

    application.container.singleton(ConnectorInterface, SqlAlchemyAsyncConnector)
    application.container.singleton(DatabaseManagerInterface, DatabaseManager)

    repository = await application.container.resolve(AsyncRepository[BarModel])

    assert isinstance(repository.session, AsyncSession)
