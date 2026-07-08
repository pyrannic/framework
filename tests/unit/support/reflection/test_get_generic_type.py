from typing import Generic, TypeVar

import pytest

from pyrannic.support.reflection import get_generic_type


T = TypeVar("T")


class __MyGenericClass(Generic[T]):
    pass


class __MyTypeClass:
    pass


class __MyClass(__MyGenericClass[__MyTypeClass]):
    pass


def test_get_generic_type__with_instance():
    """Test the get_generic_type function with a generic class instance."""
    assert get_generic_type(__MyClass()) is __MyTypeClass


def test_get_generic_type__with_class():
    """Test the get_generic_type function with a generic class."""
    assert get_generic_type(__MyClass) is __MyTypeClass


def test_get_generic_type__value_error():
    """Test the get_generic_type function with a generic class that has no generic type."""

    with pytest.raises(ValueError) as exc_info:
        get_generic_type(__MyTypeClass)

    error = str(exc_info.value)

    assert error.startswith("Generic type not found for")
    assert error.endswith("at index 0")
