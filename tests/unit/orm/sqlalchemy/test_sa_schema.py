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
from pyrannic.orm.sqlalchemy import AsyncConnector, Connector, Schema
from pyrannic.support.facades.config import Config
from tests.unit.orm.sqlalchemy.utils import BarModel


@pytest.mark.asyncio
async def test_create(application: ApplicationInterface):
    Config.set("database.connections.sqlite.driver", "sqlite")
    Config.set("database.connections.sqlite.database", ":memory:")

    application.container.singleton(ConnectorInterface, Connector)
    application.container.singleton(DatabaseManagerInterface, DatabaseManager)

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
async def test_async_create(application: ApplicationInterface):
    Config.set("database.connections.sqlite.driver", "sqlite+aiosqlite")
    Config.set("database.connections.sqlite.database", ":memory:")

    application.container.singleton(ConnectorInterface, AsyncConnector)
    application.container.singleton(DatabaseManagerInterface, DatabaseManager)

    connector = cast(
        AsyncConnector,
        await application.container.resolve(ConnectorInterface),
    )

    logger = await application.container.resolve(Logger)

    async with connector.engine.connect() as conn:
        assert not await conn.run_sync(
            lambda sync_conn: sqlalchemy.inspect(sync_conn).has_table("bars")
        )

    schema = Schema(connector.engine, logger)
    await schema.create(BarModel)

    async with connector.engine.connect() as conn:
        assert await conn.run_sync(
            lambda sync_conn: sqlalchemy.inspect(sync_conn).has_table("bars")
        )


@pytest.mark.asyncio
async def test_drop(application: ApplicationInterface):
    Config.set("database.connections.sqlite.driver", "sqlite")
    Config.set("database.connections.sqlite.database", ":memory:")

    application.container.singleton(ConnectorInterface, Connector)
    application.container.singleton(DatabaseManagerInterface, DatabaseManager)

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
async def test_async_drop(application: ApplicationInterface):
    Config.set("database.connections.sqlite.driver", "sqlite+aiosqlite")
    Config.set("database.connections.sqlite.database", ":memory:")

    application.container.singleton(ConnectorInterface, AsyncConnector)
    application.container.singleton(DatabaseManagerInterface, DatabaseManager)

    connector = cast(
        AsyncConnector,
        await application.container.resolve(ConnectorInterface),
    )

    logger = await application.container.resolve(Logger)

    schema = Schema(connector.engine, logger)
    await schema.create(BarModel)

    async with connector.engine.connect() as conn:
        assert await conn.run_sync(
            lambda sync_conn: sqlalchemy.inspect(sync_conn).has_table("bars")
        )

    await schema.drop(BarModel)

    async with connector.engine.connect() as conn:
        assert not await conn.run_sync(
            lambda sync_conn: sqlalchemy.inspect(sync_conn).has_table("bars")
        )


@pytest.mark.asyncio
async def test_log_on_exception(
    caplog: pytest.LogCaptureFixture, application: ApplicationInterface
):
    Config.set("database.connections.sqlite.database", ":memory:")

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
