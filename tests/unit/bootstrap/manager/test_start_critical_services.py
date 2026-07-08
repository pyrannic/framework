from logging import Logger

import pytest

from pyrannic.application import Application
from pyrannic.bootstrap.manager import BootstrapManager
from pyrannic.bootstrap.service_provider import ServiceProvider
from pyrannic.config.env import read_int
from pyrannic.contracts.config.respository import ConfigRepositoryInterface
from pyrannic.support.facades.facade import Facade


def test_start_critical_services__dotenv_loaded(
    manager: BootstrapManager,
    application: Application,
    critical_services: list[type[ServiceProvider]],
):
    manager.start_critical_services(application, critical_services)
    assert read_int("TEST_CRITICAL_SERVICE") == 98


def test_start_critical_services__facade_configured(
    manager: BootstrapManager,
    application: Application,
    critical_services: list[type[ServiceProvider]],
):
    manager.start_critical_services(application, critical_services)
    assert Facade.get_facade_application() is application


def test_start_critical_services__services_registered(
    manager: BootstrapManager,
    application: Application,
    critical_services: list[type[ServiceProvider]],
):
    manager.start_critical_services(application, critical_services)

    assert application.container.is_bound(ConfigRepositoryInterface)
    assert application.container.is_bound(Logger)


def test_start_critical_services__services_registered_with_aliases(
    manager: BootstrapManager,
    application: Application,
    critical_services: list[type[ServiceProvider]],
):
    manager.start_critical_services(application, critical_services)

    assert application.container.is_bound("config")
    assert application.container.is_bound("log")


def test_start_critical_services__manager_fails_if_not_started_critical_services(
    manager: BootstrapManager,
    application: Application,
):
    with pytest.raises(RuntimeError) as exc_info:
        manager.run(application)

    error = str(exc_info.value)
    assert (
        "Critical services must be started before running the bootstrap manager"
        in error
    )
