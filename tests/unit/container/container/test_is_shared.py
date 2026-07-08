from pyrannic.container.container import Container
from tests.unit.container.conftest import (
    FooImplementation,
    FooInterface,
    ScopedClass,
    SingletonClass,
)


def test_is_shared_with_instance(container: Container):
    instance = FooImplementation()
    container.instance(FooInterface, instance)

    assert container.is_shared(FooInterface)


def test_is_shared_with_scoped(container: Container):
    container.scoped(FooInterface, FooImplementation)

    assert container.is_shared(FooInterface)


def test_is_shared_with_singleton(container: Container):
    container.singleton(FooInterface, FooImplementation)

    assert container.is_shared(FooInterface)


def test_is_shared_with_bind(container: Container):
    container.bind(FooInterface, FooImplementation)

    assert not container.is_shared(FooInterface)


def test_is_shared_with_scoped_decorator(container: Container):
    assert container.is_shared(ScopedClass)


def test_is_shared_with_singleton_decorator(container: Container):
    assert container.is_shared(SingletonClass)


def test_is_shared_with_key(container: Container):
    container.singleton("abstract_key", FooImplementation)
    assert container.is_shared("abstract_key")


def test_is_shared_with_key_not_registered(container: Container):
    assert not container.is_shared("abstract_key")
