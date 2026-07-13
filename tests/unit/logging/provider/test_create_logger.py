from logging import Logger

import pytest

from pyrannic.logging.provider import LoggingServiceProvider
from pyrannic.contracts.application import ApplicationInterface
from pyrannic.support.facades.config import Config


@pytest.mark.asyncio
async def test_logging_provider(application: ApplicationInterface):
    provider = LoggingServiceProvider(application)
    provider.register()

    assert application.container.is_bound("log")
    assert application.container.is_bound(Logger)

    logger: Logger = await application.container.resolve(Logger)

    assert logger is not None
    assert logger.name == "uvicorn.error"


@pytest.mark.asyncio
async def test_custom_logging_provider(application: ApplicationInterface):
    Config.set("logging.name", "custom.logger")

    provider = LoggingServiceProvider(application)
    provider.register()

    logger: Logger = await application.container.resolve(Logger)

    assert logger is not None
    assert logger.name == "custom.logger"
