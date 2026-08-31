import pytest_asyncio

from pyrannic import Application
from pyrannic.contracts import (
    ApplicationInterface,
    DatabaseManagerInterface,
    RepositoryInterface,
)
from pyrannic.orm.sqlalchemy import Repository
from tests.unit.orm.sqlalchemy.utils import BarModel, BazsTable, FoosTable


@pytest_asyncio.fixture(scope="module")
async def application():
    application = Application(base_path="tests/application")
    yield application

    try:
        manager = await application.container.resolve(DatabaseManagerInterface)
        await manager.disconnect()
    except ValueError:
        pass


@pytest_asyncio.fixture(autouse=True)
async def init_tables(application: ApplicationInterface) -> None:
    manager = await application.container.resolve(DatabaseManagerInterface)

    await manager.rollback([FoosTable, BazsTable])
    await manager.migrate([FoosTable, BazsTable])


@pytest_asyncio.fixture()
async def repository(
    application: ApplicationInterface,
) -> RepositoryInterface[BarModel]:
    return await application.container.make(Repository[BarModel])
