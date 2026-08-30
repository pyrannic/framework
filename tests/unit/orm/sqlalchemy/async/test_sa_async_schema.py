from logging import Logger
from typing import cast

import pytest
import sqlalchemy

from pyrannic.contracts import (
    ApplicationInterface,
    ConnectorInterface,
)
from pyrannic.orm.sqlalchemy import AsyncConnector, Schema
from tests.unit.orm.sqlalchemy.utils import BarModel


@pytest.mark.asyncio
async def test_async_create(application: ApplicationInterface):
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
async def test_async_drop(application: ApplicationInterface):
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
