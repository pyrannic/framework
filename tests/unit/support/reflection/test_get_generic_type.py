from typing import Generic, TypeVar

from pyrannic.support.reflection import get_generic_type

T = TypeVar("T")


class __MyGenericClass(Generic[T]):
    pass


class __MyTypeClass:
    pass


class __MyClass(__MyGenericClass[__MyTypeClass]):
    pass


class __MyDeepClass(__MyClass):
    pass


def test_get_generic_type__with_instance():
    """Test the get_generic_type function with a generic class instance."""
    assert get_generic_type(__MyClass()) is __MyTypeClass


def test_get_generic_type__with_instance_deep_inheritance():
    """Test the get_generic_type function with a generic class instance deep in the inheritance chain."""
    assert get_generic_type(__MyDeepClass()) is __MyTypeClass


def test_get_generic_type__with_class():
    """Test the get_generic_type function with a generic class."""
    assert get_generic_type(__MyClass) is __MyTypeClass


def test_get_generic_type__with_class_deep_inheritance():
    """Test the get_generic_type function with a generic class deep in the inheritance chain."""
    assert get_generic_type(__MyDeepClass) is __MyTypeClass


def test_get_generic_type__with_not_subclass():
    """Test the get_generic_type function with a class that has no parent classes."""
    assert get_generic_type(__MyTypeClass) is None


def test_get_generic_type__with_orig_class_attr():
    """Test the get_generic_type function with a class that has the __orig_class__ attribute."""
    instance = __MyTypeClass()
    setattr(instance, "__orig_class__", __MyGenericClass[__MyTypeClass])

    assert get_generic_type(instance) is __MyTypeClass
