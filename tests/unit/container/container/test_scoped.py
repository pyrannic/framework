from fastapi.exceptions import RequestValidationError
import pytest

from pyrannic.contracts.container.container import ContainerInterface
from tests.unit.container.conftest import FooImplementation, FooInterface, ScopedClass


def test_scoped_using_type(container: ContainerInterface):
    container.scoped(FooInterface, FooImplementation)
    assert container.is_bound(FooInterface)


@pytest.mark.asyncio
async def test_scoped_using_callable(container: ContainerInterface):
    container.scoped(FooInterface, lambda app, request: FooImplementation())  # type: ignore

    instance = await container.resolve(FooInterface)

    assert container.is_bound(FooInterface)
    assert isinstance(instance, FooImplementation)


def test_scoped_invalid_concrete(container: ContainerInterface):
    with pytest.raises(RequestValidationError) as exc_info:
        container.scoped(FooInterface, "hi!")  # type: ignore

    error = str(exc_info.value)
    assert "validation error" in error
    assert "Concrete must be a class or a callable" in error


@pytest.mark.asyncio
async def test_scoped_resolves_same_instance(container: ContainerInterface):
    container.scoped(FooInterface, FooImplementation)

    instance1 = await container.resolve(FooInterface)
    instance2 = await container.resolve(FooInterface)

    assert container.is_bound(FooInterface)
    assert isinstance(instance1, FooImplementation)
    assert isinstance(instance2, FooImplementation)
    assert instance1 is instance2


@pytest.mark.asyncio
async def test_scoped_decorator(container: ContainerInterface):
    instance1 = await container.resolve(ScopedClass)
    instance2 = await container.resolve(ScopedClass)

    assert container.is_bound(ScopedClass)
    assert isinstance(instance1, ScopedClass)
    assert isinstance(instance2, ScopedClass)
    assert instance1 is instance2
