from unittest.mock import Mock

import pytest

from pyrannic.application import Application
from pyrannic.bootstrap.manager import BootstrapManager
from pyrannic.bootstrap.service_provider import ServiceProvider
from pyrannic.contracts.config.respository import ConfigRepositoryInterface
from tests.unit.bootstrap.manager.providers import (
    FooServiceProvider,
    UnbootableCriticalServiceProvider,
    UnbootableServiceProvider,
    UninitializableServiceProvider,
    UninitializableCriticalServiceProvider,
)


@pytest.mark.asyncio
async def test_lifespan__provider_lifecycle(
    application: Application,
    critical_services: list[type[ServiceProvider]],
):
    manager = BootstrapManager([FooServiceProvider])
    manager.start_critical_services(application, critical_services)
    manager.run(application)

    mock: Mock = application.container.instance("foo_service")
    config: ConfigRepositoryInterface = application.container.instance("config")

    mock.register.assert_called_once()

    async with manager.lifespan(application):
        mock.initialize.assert_called_once_with(config)
        mock.boot.assert_called_once_with(config)
        mock.failed.assert_not_called()

    mock.shutdown.assert_called_once()


@pytest.mark.asyncio
async def test_lifespan__non_critical_provider_fails_while_initializing(
    application: Application,
    critical_services: list[type[ServiceProvider]],
):
    manager = BootstrapManager([UninitializableServiceProvider])
    manager.start_critical_services(application, critical_services)
    manager.run(application)

    mock: Mock = application.container.instance("uninitializable_service")
    config: ConfigRepositoryInterface = application.container.instance("config")

    async with manager.lifespan(application):
        mock.initialize.assert_called_once_with(config)
        mock.boot.assert_called_once_with(config)
        mock.failed.assert_called_once_with("initialize")

    mock.shutdown.assert_called_once()


@pytest.mark.asyncio
async def test_lifespan__critical_provider_fails_while_initializing(
    application: Application,
    critical_services: list[type[ServiceProvider]],
):
    manager = BootstrapManager([UninitializableCriticalServiceProvider])
    manager.start_critical_services(application, critical_services)
    manager.run(application)

    mock: Mock = application.container.instance("uninitializable_critical_service")
    config: ConfigRepositoryInterface = application.container.instance("config")

    with pytest.raises(Exception) as exc_info:
        async with manager.lifespan(application):
            pass

    mock.initialize.assert_called_once_with(config)
    mock.failed.assert_not_called()
    mock.boot.assert_not_called()
    mock.shutdown.assert_not_called()

    error = str(exc_info.value)
    assert "UninitializableCriticalServiceProvider failed to initialize" in error


@pytest.mark.asyncio
async def test_lifespan__non_critical_provider_fails_while_booting(
    application: Application,
    critical_services: list[type[ServiceProvider]],
):
    manager = BootstrapManager([UnbootableServiceProvider])
    manager.start_critical_services(application, critical_services)
    manager.run(application)

    mock: Mock = application.container.instance("unbootable_service")
    config: ConfigRepositoryInterface = application.container.instance("config")

    async with manager.lifespan(application):
        mock.initialize.assert_called_once_with(config)
        mock.boot.assert_called_once_with(config)
        mock.failed.assert_called_once_with("boot")

    mock.shutdown.assert_called_once()


@pytest.mark.asyncio
async def test_lifespan__critical_provider_fails_while_booting(
    application: Application,
    critical_services: list[type[ServiceProvider]],
):
    manager = BootstrapManager([UnbootableCriticalServiceProvider])
    manager.start_critical_services(application, critical_services)
    manager.run(application)

    mock: Mock = application.container.instance("unbootable_critical_service")
    config: ConfigRepositoryInterface = application.container.instance("config")

    with pytest.raises(Exception) as exc_info:
        async with manager.lifespan(application):
            pass

    mock.initialize.assert_called_once_with(config)
    mock.boot.assert_called_once_with(config)
    mock.failed.assert_not_called()
    mock.shutdown.assert_not_called()

    error = str(exc_info.value)
    assert "UnbootableCriticalServiceProvider failed to boot" in error
