from abc import ABC
from typing import Generic, TypeVar

from pyrannic.support.reflection import is_generic_interface

T = TypeVar("T")


class GenericInterface(ABC, Generic[T]):
    pass


class NoGenericInterface(Generic[T]):
    pass


class Foo:
    pass


def test_is_generic_interface():
    assert is_generic_interface(GenericInterface[Foo])
    assert not is_generic_interface(NoGenericInterface[Foo])
