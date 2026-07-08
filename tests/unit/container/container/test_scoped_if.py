from fastapi.exceptions import RequestValidationError
import pytest

from pyrannic.contracts.container.container import ContainerInterface
from tests.unit.container.conftest import (
    FooImplementation,
    FooInterface,
    FooSecondaryImplementation,
)


@pytest.mark.asyncio
async def test_scoped_if_using_type(container: ContainerInterface):
    container.scoped_if(FooInterface, FooImplementation)
    assert container.is_bound(FooInterface)

    container.scoped_if(FooInterface, FooSecondaryImplementation)
    instance = await container.resolve(FooInterface)
    assert container.is_bound(FooInterface)
    assert isinstance(instance, FooImplementation)


@pytest.mark.asyncio
async def test_scoped_if_using_callable(container: ContainerInterface):
    container.scoped_if(FooInterface, lambda app, request: FooImplementation())  # type: ignore
    container.scoped_if(FooInterface, lambda app, request: FooSecondaryImplementation())  # type: ignore

    instance = await container.resolve(FooInterface)

    assert container.is_bound(FooInterface)
    assert isinstance(instance, FooImplementation)


def test_scoped_if_invalid_concrete(container: ContainerInterface):
    with pytest.raises(RequestValidationError) as exc_info:
        container.scoped_if(FooInterface, "hi!")  # type: ignore

    error = str(exc_info.value)
    assert "validation error" in error
    assert "Concrete must be a class or a callable" in error


@pytest.mark.asyncio
async def test_scoped_if_resolves_same_instance(container: ContainerInterface):
    container.scoped_if(FooInterface, FooImplementation)

    instance1 = await container.resolve(FooInterface)
    instance2 = await container.resolve(FooInterface)

    assert container.is_bound(FooInterface)
    assert isinstance(instance1, FooImplementation)
    assert isinstance(instance2, FooImplementation)
    assert instance1 is instance2
