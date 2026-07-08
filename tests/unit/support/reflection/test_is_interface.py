from abc import ABC, abstractmethod

from pyrannic.support.reflection import is_interface


class __MyInterface(ABC):
    pass


class __MyClass:
    pass


class __MySubInterface(__MyInterface):
    @abstractmethod
    def my_method(self):
        pass


class __MyAbstractClass(ABC):
    @abstractmethod
    def my_method(self):
        pass


class __MySubClass(__MyInterface):
    pass


def test_is_interface__check_ABC_class():
    """Test the is_interface function with an ABC class."""
    assert is_interface(__MyInterface) is True


def test_is_interface__check_non_ABC_class():
    """Test the is_interface function with a non-ABC class."""
    assert is_interface(__MyClass) is False


def test_is_interface__check_subinterface_of_ABC():
    """Test the is_interface function with a subinterface of an ABC class."""
    assert is_interface(__MySubInterface) is True


def test_is_interface__check_subclass_of_ABC():
    """Test the is_interface function with a subclass of an ABC class."""
    assert is_interface(__MySubClass) is False


def test_is_interface__check_class_with_abstract_method():
    """Test the is_interface function with a class that has some abstract method."""

    assert is_interface(__MyAbstractClass) is True
