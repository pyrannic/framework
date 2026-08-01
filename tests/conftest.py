import os

import pytest

from pyrannic.application import Application
from pyrannic.contracts import ApplicationInterface


@pytest.fixture(scope="module")
def application() -> ApplicationInterface:
    return Application(base_path="tests/application")


@pytest.fixture(scope="session", autouse=True)
def set_env():
    os.environ["DB_DATABASE"] = ":memory:"
