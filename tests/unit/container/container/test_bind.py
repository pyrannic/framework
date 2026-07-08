from fastapi.exceptions import RequestValidationError
import pytest

from pyrannic.contracts.container.container import ContainerInterface
from tests.unit.container.conftest import (
    FooImplementation,
    FooInterface,
    resolve_foo_interface,
)


def test_bind_using_type(container: ContainerInterface):
    container.bind(FooInterface, FooImplementation)
    assert container.is_bound(FooInterface)


@pytest.mark.asyncio
async def test_bind_using_callable(container: ContainerInterface):
    container.bind(FooInterface, lambda app, request: FooImplementation())  # type: ignore

    instance = await container.resolve(FooInterface)

    assert container.is_bound(FooInterface)
    assert isinstance(instance, FooImplementation)


@pytest.mark.asyncio
async def test_bind_using_async_callable(container: ContainerInterface):
    container.bind(FooInterface, resolve_foo_interface)

    instance = await container.resolve(FooInterface)

    assert container.is_bound(FooInterface)
    assert isinstance(instance, FooImplementation)


def test_bind_invalid_concrete(container: ContainerInterface):
    with pytest.raises(RequestValidationError) as exc_info:
        container.bind(FooInterface, "hi!")  # type: ignore

    error = str(exc_info.value)
    assert "validation error" in error
    assert "Concrete must be a class or a callable" in error


@pytest.mark.asyncio
async def test_bind_resolves_unique_instances(container: ContainerInterface):
    container.bind(FooInterface, FooImplementation)

    instance1 = await container.resolve(FooInterface)
    instance2 = await container.resolve(FooInterface)

    assert container.is_bound(FooInterface)
    assert isinstance(instance1, FooImplementation)
    assert isinstance(instance2, FooImplementation)
    assert instance1 is not instance2
