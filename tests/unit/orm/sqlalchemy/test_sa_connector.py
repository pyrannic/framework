from logging import Logger
from unittest.mock import Mock

import pytest
from pytest import MonkeyPatch
from sqlalchemy import URL
from sqlalchemy.ext.asyncio import AsyncEngine

from pyrannic.contracts import ApplicationInterface, ConfigRepositoryInterface
from pyrannic.orm.sqlalchemy import AsyncConnector, Connector


@pytest.mark.asyncio
async def test_connector_disconnect(
    application: ApplicationInterface,
    monkeypatch: MonkeyPatch,
) -> None:
    container = application.container
    connector = Connector(
        application,
        await container.resolve(Logger),
        await container.resolve("config"),
    )

    mock = Mock()

    monkeypatch.setattr(connector, "_engine", mock)

    await connector.disconnect()
    mock.dispose.assert_called_once()


@pytest.mark.asyncio
async def test_async_connector_disconnect(
    application: ApplicationInterface,
    monkeypatch: MonkeyPatch,
) -> None:
    container = application.container
    connector = AsyncConnector(
        application,
        await container.resolve(Logger),
        await container.resolve("config"),
    )

    mock = Mock(spec=AsyncEngine)

    monkeypatch.setattr(connector, "_engine", mock)

    await connector.disconnect()
    mock.dispose.assert_called_once()


@pytest.mark.asyncio
async def test_connector_url_using_sqlite_database_file(
    application: ApplicationInterface,
):
    config = application.container.instance(ConfigRepositoryInterface)
    config.set("database.connections.sqlite.url", None)
    config.set("database.connections.sqlite.database", "database/database.sqlite")

    connector = Connector(
        application,
        await application.container.resolve(Logger),
        config,
    )

    assert isinstance(connector.url, URL)
    assert (
        connector.url.render_as_string(hide_password=False)
        == "sqlite:///database/database.sqlite"
    )


@pytest.mark.asyncio
async def test_abstract_connector_url_is_an_url_object(
    application: ApplicationInterface,
) -> None:
    container = application.container

    config = container.instance(ConfigRepositoryInterface)
    config.set("database.connections.sqlite.url", None)

    connector = Connector(
        application,
        await container.resolve(Logger),
        await container.resolve("config"),
    )

    assert isinstance(connector.url, URL)


@pytest.mark.asyncio
async def test_abstract_connector_url_is_an_url_object_with_config(
    application: ApplicationInterface,
) -> None:
    db_url = "sqlite+aiosqlite:///test.db"
    container = application.container
    config = await container.resolve(ConfigRepositoryInterface)

    orig = config.get("database.connections.sqlite.url")
    config.set("database.connections.sqlite.url", db_url)

    connector = Connector(
        application,
        await container.resolve(Logger),
        config,
    )

    assert isinstance(connector.url, str)
    assert connector.url == db_url
    config.set("database.connections.sqlite.url", orig)
