import os

import pytest_asyncio

from pyrannic import Application
from pyrannic.contracts import DatabaseManagerInterface


@pytest_asyncio.fixture(scope="module")
async def application():
    os.environ["APP_ENV"] = "async-tests"

    application = Application(base_path="tests/application")
    yield application

    try:
        manager = await application.container.resolve(DatabaseManagerInterface)
        await manager.disconnect()
    except ValueError:
        pass

    os.environ["APP_ENV"] = "tests"
