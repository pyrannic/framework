from unittest.mock import Mock

import pytest

from pyrannic.application import Application
from pyrannic.bootstrap.manager import BootstrapManager
from pyrannic.contracts.database.connector import ConnectorInterface
from pyrannic.contracts.database.manager import DatabaseManagerInterface
from pyrannic.database.manager import DatabaseManager
from pyrannic.database.provider import DatabaseServiceProvider
from pyrannic.orm.sqlalchemy.connector import SqlAlchemyConnector
from tests.unit.database.utils import MockDatabaseServiceProvider


@pytest.mark.asyncio
async def test_register_singletons():
    application = Application()
    bootstrap_manager = BootstrapManager([DatabaseServiceProvider])

    bootstrap_manager.start_critical_services(application, [])
    bootstrap_manager.run(application)

    connector_1 = await application.container.resolve(ConnectorInterface)
    manager_1 = await application.container.resolve(DatabaseManagerInterface)

    assert isinstance(connector_1, SqlAlchemyConnector)
    assert isinstance(manager_1, DatabaseManager)

    connector_2 = await application.container.resolve(ConnectorInterface)
    manager_2 = await application.container.resolve(DatabaseManagerInterface)

    assert connector_1 is connector_2
    assert manager_1 is manager_2


@pytest.mark.asyncio
async def test_boot_called():
    application = Application()
    bootstrap_manager = BootstrapManager([MockDatabaseServiceProvider])

    bootstrap_manager.start_critical_services(application, [])
    bootstrap_manager.run(application)

    mock: Mock = application.container.instance("MockDatabaseServiceProvider")
    manager = await application.container.resolve(DatabaseManagerInterface)

    mock.register.assert_called_once()

    async with bootstrap_manager.lifespan(application):
        mock.initialize.assert_called_once()
        mock.is_critical.assert_called()
        mock.boot.assert_called_once_with(manager)
        mock.failed.assert_not_called()

    mock.shutdown.assert_called_once_with(manager)
