import pytest

from pyrannic.contracts.container.container import ContainerInterface
from pyrannic.support.reflection import get_generic_type
from tests.unit.container.conftest import (
    BazServiceWithParams,
    FooGeneric,
    FooGenericImplementation,
    FooGenericInterface,
    FooImplementation,
    FooInterface,
    FooModel,
    FooSecondaryImplementation,
    SubFooGenericImplementation,
    SubFooModel,
)


@pytest.mark.asyncio
async def test_make_concrete_class(container: ContainerInterface):
    instance = await container.make(FooSecondaryImplementation)

    assert not container.is_bound(FooSecondaryImplementation)
    assert isinstance(instance, FooSecondaryImplementation)


@pytest.mark.asyncio
async def test_make_generic_class(container: ContainerInterface):
    instance = await container.make(FooGeneric[FooModel])

    assert not container.is_bound(FooGeneric[FooModel])
    assert isinstance(instance, FooGeneric)
    assert get_generic_type(instance) == FooModel


@pytest.mark.asyncio
async def test_make_with_positional_parameters(container: ContainerInterface):
    instance = await container.make(BazServiceWithParams, "value1", "value2")

    assert not container.is_bound(BazServiceWithParams)
    assert isinstance(instance, BazServiceWithParams)
    assert instance.value1 == "value1"
    assert instance.value2 == "value2"
    assert isinstance(instance.foo_service, FooImplementation)


@pytest.mark.asyncio
async def test_make_with_named_parameters(container: ContainerInterface):
    instance = await container.make(
        BazServiceWithParams, value1="value1", value2="value2"
    )

    assert not container.is_bound(BazServiceWithParams)
    assert isinstance(instance, BazServiceWithParams)
    assert instance.value1 == "value1"
    assert instance.value2 == "value2"
    assert isinstance(instance.foo_service, FooImplementation)


@pytest.mark.asyncio
async def test_make_with_mixed_parameters(container: ContainerInterface):
    instance = await container.make(BazServiceWithParams, "value1", value2="value2")

    assert not container.is_bound(BazServiceWithParams)
    assert isinstance(instance, BazServiceWithParams)
    assert instance.value1 == "value1"
    assert instance.value2 == "value2"
    assert isinstance(instance.foo_service, FooImplementation)


@pytest.mark.asyncio
async def test_make_with_interface_not_bound(container: ContainerInterface):
    with pytest.raises(RuntimeError) as exc_info:
        await container.make(FooInterface)

    error = str(exc_info.value)
    assert "No binding found for interface FooInterface" in error


@pytest.mark.asyncio
async def test_make_with_key_not_bound(container: ContainerInterface):
    with pytest.raises(RuntimeError) as exc_info:
        await container.make("FooInterface")

    error = str(exc_info.value)
    assert "No binding found for key FooInterface" in error


@pytest.mark.asyncio
async def test_make_with_generic_interface(container: ContainerInterface):
    container.bind(FooGenericInterface[FooModel], FooGenericImplementation)
    instance = await container.make(FooGenericInterface[FooModel])

    assert container.is_bound(FooGenericInterface[FooModel])
    assert isinstance(instance, FooGenericImplementation)


@pytest.mark.asyncio
async def test_make_with_generic_interface_subclass(container: ContainerInterface):
    container.bind(FooGenericInterface[FooModel], SubFooGenericImplementation)
    instance = await container.make(FooGenericInterface[SubFooModel])

    assert container.is_bound(FooGenericInterface[FooModel])
    assert isinstance(instance, SubFooGenericImplementation)


@pytest.mark.asyncio
async def test_make_with_generic_interface_subclass_raising_error(
    container: ContainerInterface,
):
    with pytest.raises(RuntimeError) as exc_info:
        await container.make(FooGenericInterface[SubFooModel])

    error = str(exc_info.value)
    assert "No binding found for generic interface FooGenericInterface" in error
