from typing import Any, Generator

import pytest
from starlette.testclient import TestClient

from pyrannic.application import Application
from pyrannic.contracts.application import ApplicationInterface


@pytest.fixture(scope="module")
def application() -> ApplicationInterface:
    return Application(base_path="tests/application")


@pytest.fixture(scope="module")
def http_client(
    application: ApplicationInterface,
) -> Generator[TestClient, Any, Any]:
    with TestClient(application) as client:
        yield client
