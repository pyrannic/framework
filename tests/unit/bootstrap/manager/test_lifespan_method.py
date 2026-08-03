from unittest.mock import Mock

import pytest

from pyrannic.application import Application
from pyrannic.bootstrap.manager import BootstrapManager
from pyrannic.bootstrap.service_provider import ServiceProvider
from pyrannic.contracts.config.repository import ConfigRepositoryInterface
from tests.unit.bootstrap.manager.providers import (
    CustomExceptionServiceProvider,
    FooServiceProvider,
    ServiceProviderRaiseRuntimeErrorOnBoot,
    ServiceProviderRaiseRuntimeErrorOnInitialize,
    UnbootableCriticalServiceProvider,
    UnbootableServiceProvider,
    UninitializableCriticalServiceProvider,
    UninitializableServiceProvider,
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
    caplog: pytest.LogCaptureFixture,
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
    assert "UninitializableCriticalServiceProvider initialize method called" in error
    assert "UninitializableCriticalServiceProvider failed to initialize" in caplog.text


@pytest.mark.asyncio
async def test_lifespan__critical_provider_fails_when_raise_runtime_error(
    application: Application,
    critical_services: list[type[ServiceProvider]],
    caplog: pytest.LogCaptureFixture,
):
    manager = BootstrapManager([ServiceProviderRaiseRuntimeErrorOnInitialize])
    manager.start_critical_services(application, critical_services)
    manager.run(application)

    mock: Mock = application.container.instance(
        "service_provider_raise_runtime_error_on_initialize"
    )
    config: ConfigRepositoryInterface = application.container.instance("config")

    with pytest.raises(Exception) as exc_info:
        async with manager.lifespan(application):
            pass

    mock.initialize.assert_called_once_with(config)
    mock.failed.assert_not_called()
    mock.boot.assert_not_called()
    mock.shutdown.assert_not_called()

    error = str(exc_info.value)
    assert (
        "ServiceProviderRaiseRuntimeErrorOnInitialize initialize method called" in error
    )
    assert (
        "ServiceProviderRaiseRuntimeErrorOnInitialize failed to initialize"
        in caplog.text
    )


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
    caplog: pytest.LogCaptureFixture,
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
    assert "UnbootableCriticalServiceProvider boot method called" in error
    assert "UnbootableCriticalServiceProvider failed to boot" in caplog.text


@pytest.mark.asyncio
async def test_lifespan__non_critical_provider_fails_when_raise_runtime_error(
    application: Application,
    critical_services: list[type[ServiceProvider]],
    caplog: pytest.LogCaptureFixture,
):
    manager = BootstrapManager([ServiceProviderRaiseRuntimeErrorOnBoot])
    manager.start_critical_services(application, critical_services)
    manager.run(application)

    mock: Mock = application.container.instance(
        "service_provider_raise_runtime_error_on_boot"
    )
    config: ConfigRepositoryInterface = application.container.instance("config")

    with pytest.raises(Exception) as exc_info:
        async with manager.lifespan(application):
            mock.initialize.assert_called_once_with(config)
            mock.boot.assert_called_once_with(config)
            mock.failed.assert_called_once_with("boot")

    mock.initialize.assert_called_once_with(config)
    mock.boot.assert_called_once_with(config)
    mock.failed.assert_not_called()
    mock.shutdown.assert_not_called()

    error = str(exc_info.value)
    assert "ServiceProviderRaiseRuntimeErrorOnBoot boot method called" in error
    assert "ServiceProviderRaiseRuntimeErrorOnBoot failed to boot" in caplog.text


@pytest.mark.asyncio
async def test_lifespan__provider_fails_raising_custom_error(
    application: Application,
    critical_services: list[type[ServiceProvider]],
    caplog: pytest.LogCaptureFixture,
):
    manager = BootstrapManager([CustomExceptionServiceProvider])
    manager.start_critical_services(application, critical_services)
    manager.run(application)

    mock: Mock = application.container.instance("custom_exception_service")
    config: ConfigRepositoryInterface = application.container.instance("config")

    with pytest.raises(Exception) as exc_info:
        async with manager.lifespan(application):
            mock.initialize.assert_called_once_with(config)
            mock.boot.assert_called_once_with(config)
            mock.failed.assert_called_once_with("boot")

    mock.initialize.assert_called_once_with(config)
    mock.boot.assert_called_once_with(config)
    mock.failed.assert_not_called()
    mock.shutdown.assert_not_called()
    mock.exception.assert_called_once()

    error = str(exc_info.value)
    assert "CustomExceptionServiceProvider exception method called" in error
    assert "CustomExceptionServiceProvider failed to boot" in caplog.text
