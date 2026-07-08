import pytest

from pyrannic.application import Application
from pyrannic.bootstrap.manager import BootstrapManager
from pyrannic.bootstrap.service_provider import ServiceProvider
from pyrannic.config.provider import ConfigRepositoryProvider
from pyrannic.logging.provider import LoggingServiceProvider


@pytest.fixture()
def application() -> Application:
    return Application(base_path="tests/unit/bootstrap/manager")


@pytest.fixture()
def critical_services() -> list[type[ServiceProvider]]:
    return [
        ConfigRepositoryProvider,
        LoggingServiceProvider,
    ]


@pytest.fixture()
def manager() -> BootstrapManager:
    return BootstrapManager()


@pytest.fixture()
def manager_started(
    application: Application,
    critical_services: list[type[ServiceProvider]],
) -> BootstrapManager:
    manager = BootstrapManager()
    return manager.start_critical_services(application, critical_services)
