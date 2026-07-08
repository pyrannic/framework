from unittest.mock import Mock

import pytest

from pyrannic.application import Application
from pyrannic.bootstrap.manager import BootstrapManager
from pyrannic.bootstrap.service_provider import ServiceProvider
from tests.unit.bootstrap.manager.providers import (
    BarServiceProvider,
    BazServiceProvider,
    FooServiceProvider,
    ServiceProviderWithBindings,
    ServiceProviderWithSingletons,
)


def test_run__successful(
    application: Application,
    critical_services: list[type[ServiceProvider]],
):
    manager = BootstrapManager([FooServiceProvider])
    manager.start_critical_services(application, critical_services)
    manager.run(application)

    assert application.container.is_bound("foo_service")

    mock: Mock = application.container.instance("foo_service")
    mock.register.assert_called_once()
    mock.initialize.assert_not_called()
    mock.boot.assert_not_called()
    mock.failed.assert_not_called()
    mock.shutdown.assert_not_called()


def test_run__non_critical_provider_fails_while_registering(
    application: Application,
    critical_services: list[type[ServiceProvider]],
):
    manager = BootstrapManager([FooServiceProvider, BarServiceProvider])
    manager.start_critical_services(application, critical_services)
    manager.run(application)

    assert application.container.is_bound("bar_service")

    mock: Mock = application.container.instance("bar_service")

    mock.register.assert_called_once()
    mock.initialize.assert_not_called()
    mock.boot.assert_not_called()
    mock.shutdown.assert_not_called()
    mock.failed.assert_called_once_with("register")


def test_run__critical_provider_fails_while_registering(
    application: Application,
    critical_services: list[type[ServiceProvider]],
):
    manager = BootstrapManager(
        [FooServiceProvider, BarServiceProvider, BazServiceProvider]
    )
    manager.start_critical_services(application, critical_services)

    with pytest.raises(Exception) as exc_info:
        manager.run(application)

    mock: Mock = application.container.instance("baz_service")

    mock.register.assert_called_once()
    mock.initialize.assert_not_called()
    mock.boot.assert_not_called()
    mock.failed.assert_not_called()
    mock.shutdown.assert_not_called()

    error = str(exc_info.value)
    assert "BazServiceProvider failed to register" in error


def test_run__provider_register_using_bindings_property(
    application: Application,
    critical_services: list[type[ServiceProvider]],
):
    manager = BootstrapManager([ServiceProviderWithBindings])
    manager.start_critical_services(application, critical_services)
    manager.run(application)

    assert application.container.is_bound("foo_service")
    assert application.container.is_bound("bar_service")
    assert application.container.is_bound("baz_service")


def test_run__provider_register_using_singletons_property(
    application: Application,
    critical_services: list[type[ServiceProvider]],
):
    manager = BootstrapManager([ServiceProviderWithSingletons])
    manager.start_critical_services(application, critical_services)
    manager.run(application)

    assert application.container.is_bound("foo_singleton")
    assert application.container.is_bound("bar_singleton")
    assert application.container.is_bound("baz_singleton")


def test_run__provider_container_is_equal_to_application_container(
    application: Application,
    critical_services: list[type[ServiceProvider]],
):
    manager = BootstrapManager([FooServiceProvider])
    manager.start_critical_services(application, critical_services)
    manager.run(application)

    mock: Mock = application.container.instance("foo_service")

    assert mock.container == application.container
