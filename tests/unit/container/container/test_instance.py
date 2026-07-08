import pytest

from pyrannic.contracts.container.container import ContainerInterface
from tests.unit.container.conftest import FooImplementation, FooInterface


def test_instance(container: ContainerInterface):
    instance = FooImplementation()
    container.instance(FooInterface, instance)

    instance1 = container.instance(FooInterface)

    assert container.is_bound(FooInterface)
    assert isinstance(instance1, FooImplementation)
    assert instance is instance1


def test_instance_overrides_previous_binding(container: ContainerInterface):
    container.bind(FooInterface, FooImplementation)

    instance = FooImplementation()
    container.instance(FooInterface, instance)

    instance1 = container.instance(FooInterface)

    assert container.is_bound(FooInterface)
    assert isinstance(instance1, FooImplementation)
    assert instance is instance1


def test_instance_overrides_previous_scoped(container: ContainerInterface):
    container.scoped(FooInterface, FooImplementation)

    instance = FooImplementation()
    container.instance(FooInterface, instance)

    instance1 = container.instance(FooInterface)

    assert container.is_bound(FooInterface)
    assert isinstance(instance1, FooImplementation)
    assert instance is instance1


def test_instance_overrides_previous_instance(container: ContainerInterface):
    instance = FooImplementation()
    container.instance(FooInterface, instance)

    instance2 = FooImplementation()
    container.instance(FooInterface, instance2)

    instance1 = container.instance(FooInterface)

    assert container.is_bound(FooInterface)
    assert isinstance(instance1, FooImplementation)
    assert instance2 is instance1


def test_instance_overrides_previous_singleton(container: ContainerInterface):
    container.singleton(FooInterface, FooImplementation)

    instance = FooImplementation()
    container.instance(FooInterface, instance)

    instance1 = container.instance(FooInterface)

    assert container.is_bound(FooInterface)
    assert isinstance(instance1, FooImplementation)
    assert instance is instance1


@pytest.mark.asyncio
async def test_instance_also_can_be_resolved(container: ContainerInterface):
    instance = FooImplementation()
    container.instance(FooInterface, instance)

    instance1 = await container.resolve(FooInterface)

    assert container.is_bound(FooInterface)
    assert isinstance(instance1, FooImplementation)
    assert instance is instance1


def test_instance_not_bound(container: ContainerInterface):
    with pytest.raises(ValueError) as exc_info:
        container.instance(FooInterface)

    error = str(exc_info.value)
    assert "No instance found for FooInterface" in error
