import pytest

from pyrannic.config.env import read_bool


def test_read_bool():
    assert read_bool("FOO_DEBUG")


def test_read_bool_with_default():
    assert read_bool("APP_DEBUG", default=True)


def test_read_bool_not_found():
    assert read_bool("APP_DEBUG") is True


def test_read_bool_no_value():
    assert read_bool("FOO_SESSION_HTTP_ONLY") is False


def test_read_bool_invalid_value_error():
    with pytest.raises(ValueError) as exc_info:
        read_bool("FOO_NAME")

    error = str(exc_info.value)
    assert "Invalid boolean value for FOO_NAME: MyFooApp" in error
