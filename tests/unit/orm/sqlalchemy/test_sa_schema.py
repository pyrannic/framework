from logging import Logger
from typing import cast

import pytest
import sqlalchemy

from pyrannic.contracts import (
    ApplicationInterface,
    ConnectorInterface,
    DatabaseManagerInterface,
)
from pyrannic.database.manager import DatabaseManager
from pyrannic.orm.sqlalchemy import Connector, Schema
from pyrannic.support.facades.config import Config
from tests.unit.orm.sqlalchemy.utils import BarModel


@pytest.mark.asyncio
async def test_create(application: ApplicationInterface):
    connector = cast(
        Connector,
        await application.container.resolve(ConnectorInterface),
    )

    logger = await application.container.resolve(Logger)

    assert not sqlalchemy.inspect(connector.engine).has_table("bars")

    schema = Schema(connector.engine, logger)
    await schema.create(BarModel)

    assert sqlalchemy.inspect(connector.engine).has_table("bars")


@pytest.mark.asyncio
async def test_drop(application: ApplicationInterface):
    connector = cast(
        Connector,
        await application.container.resolve(ConnectorInterface),
    )

    logger = await application.container.resolve(Logger)

    schema = Schema(connector.engine, logger)
    await schema.create(BarModel)

    assert sqlalchemy.inspect(connector.engine).has_table("bars")

    await schema.drop(BarModel)

    assert not sqlalchemy.inspect(connector.engine).has_table("bars")


@pytest.mark.asyncio
async def test_log_on_exception(
    caplog: pytest.LogCaptureFixture,
    application: ApplicationInterface,
):
    # Use a driver that will raise an exception when trying to create/drop the table
    Config.set("database.connections.sqlite.url", "sqlite+aiosqlite:///:memory:")

    application.container.singleton(ConnectorInterface, Connector)
    application.container.singleton(DatabaseManagerInterface, DatabaseManager)

    connector = cast(
        Connector,
        await application.container.resolve(ConnectorInterface),
    )

    logger = await application.container.resolve(Logger)

    schema = Schema(connector.engine, logger)

    await schema.create(BarModel)
    assert "Failed to create bars table:" in caplog.text

    await schema.drop(BarModel)
    assert "Failed to drop bars table:" in caplog.text

    Config.set("database.connections.sqlite.driver", "sqlite")
