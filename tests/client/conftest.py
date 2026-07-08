from starlette.testclient import TestClient
import pytest

from pyrannic.application import Application
from pyrannic.contracts.application import ApplicationInterface


@pytest.fixture(scope="module")
def application() -> ApplicationInterface:
    return Application(base_path="tests/application")


@pytest.fixture(scope="module")
def http_client(application: ApplicationInterface) -> TestClient:
    return TestClient(application)
