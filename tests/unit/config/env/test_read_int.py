import pytest

from pyrannic.config.env import read_int


def test_read_int():
    assert read_int("FOO_SESSION_LIFETIME") == 120


def test_read_int_with_default():
    assert read_int("SESSION_LIFETIME", default=42) == 42


def test_read_int_not_found():
    assert read_int("SESSION_LIFETIME") == 0


def test_read_int_invalid_value_error():
    with pytest.raises(ValueError) as exc_info:
        read_int("FOO_NAME")

    error = str(exc_info.value)
    assert "Invalid integer value for FOO_NAME: MyFooApp" in error
