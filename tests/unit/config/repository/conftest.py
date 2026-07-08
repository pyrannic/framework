import pytest

from pyrannic.config.repository import ConfigRepository
from pyrannic.contracts.config.respository import ConfigRepositoryInterface


@pytest.fixture()
def repository() -> ConfigRepositoryInterface:
    return ConfigRepository(
        {
            "database": {
                "host": "localhost",
                "port": 5432,
                "username": "user",
                "password": "pass",
            },
            "app": {
                "name": "MyApp",
                "debug": True,
                "secret_key": "supersecret",
            },
            "foo": {
                "integer_str": "42",
                "float": 3.14,
                "float_str": "2.718",
                "boolean": True,
                "boolean_true": "true",
                "boolean_True": "True",
                "boolean_TRUE": "TRUE",
                "boolean_false": "false",
                "boolean_False": "False",
                "boolean_FALSE": "FALSE",
                "boolean_one": "1",
                "boolean_zero": "0",
                "boolean_yes": "yes",
                "boolean_Yes": "Yes",
                "boolean_YES": "YES",
                "boolean_no": "no",
                "boolean_No": "No",
                "boolean_NO": "NO",
                "boolean_int_0": 0,
                "boolean_int_1": 1,
                "list": [1, 2, 3],
            },
        }
    )
