import pytest

from pyrannic.config.provider import ConfigRepositoryProvider
from pyrannic.contracts.application import ApplicationInterface
from pyrannic.contracts.config.respository import ConfigRepositoryInterface


@pytest.mark.asyncio
async def test_provider(application: ApplicationInterface):
    provider = ConfigRepositoryProvider(application)
    provider.register()

    assert application.container.is_bound("config")

    config: ConfigRepositoryInterface = await application.container.resolve("config")

    assert config is not None
    assert config.string("app.name") == "Testing PyrannicApp"
