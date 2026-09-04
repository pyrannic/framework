import pytest
from fastapi import Request

from pyrannic.contracts import ApplicationInterface, ContainerInterface
from tests.unit.container.conftest import (
    BarGenericInterface,
    BarImplementation,
    FooImplementation,
    FooInterface,
    ResolverClass,
    resolve_foo_interface,
)


def test_bind_using_type(container: ContainerInterface):
    container.bind(FooInterface, FooImplementation)
    assert container.is_bound(FooInterface)


@pytest.mark.asyncio
async def test_bind_using_lambda(container: ContainerInterface):
    container.bind(FooInterface, lambda app, request: FooImplementation())  # type: ignore

    instance = await container.resolve(FooInterface)

    assert container.is_bound(FooInterface)
    assert isinstance(instance, FooImplementation)


@pytest.mark.asyncio
async def test_bind_generic_interface_using_lambda(container: ContainerInterface):
    container.bind(
        BarGenericInterface[FooInterface],
        lambda app, request: BarImplementation(),  # type: ignore
    )

    with pytest.raises(RuntimeError) as exc_info:
        await container.resolve(BarGenericInterface[FooImplementation])

    error = str(exc_info.value)
    assert "Cannot determine the return type of the function" in error
    assert "If you are using a lambda function" in error
    assert "If you are using a regular function" in error


@pytest.mark.asyncio
async def test_bind_generic_interface_using_function(container: ContainerInterface):
    def _resolve_bar_generic_interface(
        app: ApplicationInterface,
        request: Request,
    ) -> BarGenericInterface[FooInterface]:
        return BarImplementation()

    container.bind(BarGenericInterface[FooInterface], _resolve_bar_generic_interface)
    instance = await container.resolve(BarGenericInterface[FooImplementation])

    assert container.is_bound(BarGenericInterface[FooInterface])
    assert isinstance(instance, BarImplementation)


@pytest.mark.asyncio
async def test_bind_using_instance_method(container: ContainerInterface):
    container.bind(FooInterface, ResolverClass().resolve_instancemethod)

    instance = await container.resolve(FooInterface)

    assert container.is_bound(FooInterface)
    assert isinstance(instance, FooImplementation)


@pytest.mark.asyncio
async def test_bind_using_class_method(container: ContainerInterface):
    container.bind(FooInterface, ResolverClass.resolve_classmethod)

    instance = await container.resolve(FooInterface)

    assert container.is_bound(FooInterface)
    assert isinstance(instance, FooImplementation)


@pytest.mark.asyncio
async def test_bind_using_static_method(container: ContainerInterface):
    container.bind(FooInterface, ResolverClass.resolve_staticmethod)

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
    with pytest.raises(ValueError) as exc_info:
        container.bind(FooInterface, "hi!")  # type: ignore

    error = str(exc_info.value)
    assert "Concrete hi! must be a class or a callable" in error


@pytest.mark.asyncio
async def test_bind_resolves_unique_instances(container: ContainerInterface):
    container.bind(FooInterface, FooImplementation)

    instance1 = await container.resolve(FooInterface)
    instance2 = await container.resolve(FooInterface)

    assert container.is_bound(FooInterface)
    assert isinstance(instance1, FooImplementation)
    assert isinstance(instance2, FooImplementation)
    assert instance1 is not instance2
