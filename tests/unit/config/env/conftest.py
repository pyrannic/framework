import os

from dotenv import load_dotenv
import pytest


@pytest.fixture(autouse=True)
def load_env_file():
    """
    Load the .test_env file before running tests.
    """

    env_path = os.path.join(os.path.dirname(__file__), ".test_env")
    load_dotenv(env_path)
    yield
