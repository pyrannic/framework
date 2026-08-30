from collections.abc import Generator
from typing import Any

import pytest
import pytest_asyncio
from starlette.testclient import TestClient

from pyrannic import Application
from pyrannic.contracts import ApplicationInterface, DatabaseManagerInterface


@pytest_asyncio.fixture(scope="module")
async def application():
    application = Application(base_path="tests/application")
    yield application
    manager = await application.container.resolve(DatabaseManagerInterface)
    await manager.disconnect()


@pytest.fixture(scope="module")
def http_client(application: ApplicationInterface) -> Generator[TestClient, Any, Any]:
    with TestClient(application) as client:
        yield client
