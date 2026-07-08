from fastapi.exceptions import RequestValidationError
import pytest

from pyrannic.contracts.container.container import ContainerInterface
from tests.unit.container.conftest import (
    FooImplementation,
    FooInterface,
    SingletonClass,
)


def test_singleton_using_type(container: ContainerInterface):
    container.singleton(FooInterface, FooImplementation)
    assert container.is_bound(FooInterface)


@pytest.mark.asyncio
async def test_singleton_using_callable(container: ContainerInterface):
    container.singleton(FooInterface, lambda app, request: FooImplementation())  # type: ignore

    instance = await container.resolve(FooInterface)

    assert container.is_bound(FooInterface)
    assert isinstance(instance, FooImplementation)


def test_singleton_invalid_concrete(container: ContainerInterface):
    with pytest.raises(RequestValidationError) as exc_info:
        container.singleton(FooInterface, "hi!")  # type: ignore

    error = str(exc_info.value)
    assert "validation error" in error
    assert "Concrete must be a class or a callable" in error


@pytest.mark.asyncio
async def test_singleton_resolves_same_instance(container: ContainerInterface):
    container.singleton(FooInterface, FooImplementation)

    instance1 = await container.resolve(FooInterface)
    instance2 = await container.resolve(FooInterface)

    assert container.is_bound(FooInterface)
    assert isinstance(instance1, FooImplementation)
    assert isinstance(instance2, FooImplementation)
    assert instance1 is instance2


@pytest.mark.asyncio
async def test_singleton_decorator(container: ContainerInterface):
    instance1 = await container.resolve(SingletonClass)
    instance2 = await container.resolve(SingletonClass)

    assert container.is_bound(SingletonClass)
    assert isinstance(instance1, SingletonClass)
    assert isinstance(instance2, SingletonClass)
    assert instance1 is instance2
