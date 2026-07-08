from logging import Logger
from unittest.mock import Mock

import pytest

from pyrannic.contracts.application import ApplicationInterface
from tests.unit.bootstrap.instance_service_provider.providers import (
    InstanceServiceProvider,
    InstanceServiceProviderWithDependencies,
)


@pytest.mark.asyncio
async def test_instance_service_provider__register(application: ApplicationInterface):
    provider = InstanceServiceProvider(application)
    provider.register()

    assert application.container.is_bound(Mock)
    mock: Mock = await application.container.resolve(Mock)

    assert isinstance(mock, Mock)


@pytest.mark.asyncio
async def test_instance_service_provider__aliases(application: ApplicationInterface):
    provider = InstanceServiceProvider(application)
    provider.register()

    mock: Mock = await application.container.resolve(Mock)

    for alias in provider.aliases:
        assert application.container.is_bound(alias)
        instance: Mock = await application.container.resolve(alias)  # type: ignore

        assert instance == mock


@pytest.mark.asyncio
async def test_instance_service_provider__with_dependencies(
    application: ApplicationInterface,
):
    provider = InstanceServiceProviderWithDependencies(application)
    await provider.boot()

    assert application.container.is_bound(Mock)
    mock: Mock = await application.container.resolve(Mock)
    assert isinstance(mock, Mock)

    logger: Logger = await application.container.resolve(Logger)
    mock.create.assert_called_once_with(logger)
