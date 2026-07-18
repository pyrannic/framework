import os

import pytest

from pyrannic.application import Application
from pyrannic.contracts.application import ApplicationInterface


@pytest.fixture(scope="module")
def application() -> ApplicationInterface:
    return Application(base_path="tests/application")


@pytest.fixture(scope="session", autouse=True)
def database_management():
    """
    Create a temporary sqlite database for testing purposes. The database will be created before the tests run and deleted after the tests are completed.
    This fixture is automatically used in all tests, so you don't need to explicitly include it in your test functions.
    """

    _refresh_database()
    yield
    _delete_database()


def _refresh_database():
    """
    Refresh the temporary sqlite database for testing purposes.
    This function deletes the existing database and creates a new one.
    """
    _delete_database()
    _create_database()


def _create_database():
    """
    Create a temporary sqlite database for testing purposes.
    """
    try:
        file = open("tests/application/database/database.sqlite", "x")
        file.close()
    except FileExistsError:
        # If the file already exists, we don't need to create it again.
        pass


def _delete_database():
    """
    Delete the temporary sqlite database after testing.
    """
    try:
        os.remove("tests/application/database/database.sqlite")
    except FileNotFoundError:
        # If the file does not exist, we don't need to delete it.
        pass
