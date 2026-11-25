import os

import pytest
from dotenv import load_dotenv

from tests.unit.config.configuration.foo import Foo
from tests.unit.config.configuration.foo_config import FooBarConfig, FooConfig


@pytest.fixture(scope="module")
def foo(env_path: str) -> Foo:
    return Foo(_env_file=env_path)  # type: ignore


@pytest.fixture(scope="module")
def foo_config() -> FooConfig:
    return FooConfig()


@pytest.fixture(scope="module")
def foo_bar_config() -> FooBarConfig:
    return FooBarConfig()


@pytest.fixture(scope="module")
def env_path() -> str:
    return os.path.join(os.path.dirname(__file__), ".test_env")


@pytest.fixture(autouse=True)
def load_env_file(env_path: str):
    """
    Load the .test_env file before running tests.
    """

    load_dotenv(env_path)
    yield
