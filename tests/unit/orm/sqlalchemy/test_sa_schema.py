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
