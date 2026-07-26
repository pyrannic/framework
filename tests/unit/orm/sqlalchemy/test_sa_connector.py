from logging import Logger
from unittest.mock import Mock

import pytest
from pytest import MonkeyPatch
from sqlalchemy.ext.asyncio import AsyncEngine

from pyrannic.contracts import ApplicationInterface
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
