import pytest

from pyrannic.application import Application
from pyrannic.contracts.application import ApplicationInterface


@pytest.fixture(scope="module")
def application() -> ApplicationInterface:
    return Application(base_path="tests/unit/http/providers/application")


@pytest.fixture(scope="module")
def app_no_providers() -> ApplicationInterface:
    return Application(base_path="tests/unit/http/providers/application_no_providers")
