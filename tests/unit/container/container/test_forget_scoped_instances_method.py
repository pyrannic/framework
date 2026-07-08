import pytest

from pyrannic.container.container import Container
from tests.unit.container.conftest import FooImplementation, FooInterface


@pytest.mark.asyncio
async def test_forget_scoped_instances(container: Container):
    container.scoped(FooInterface, FooImplementation)

    instance1 = await container.resolve(FooInterface)
    container.forget_scoped_instances()
    instance2 = await container.resolve(FooInterface)

    assert container.is_bound(FooInterface)
    assert isinstance(instance1, FooImplementation)
    assert isinstance(instance2, FooImplementation)
    assert instance1 is not instance2


@pytest.mark.asyncio
async def test_forget_scoped_instances_with_singleton(container: Container):
    container.singleton(FooInterface, FooImplementation)

    instance1 = await container.resolve(FooInterface)
    container.forget_scoped_instances()
    instance2 = await container.resolve(FooInterface)

    assert container.is_bound(FooInterface)
    assert isinstance(instance1, FooImplementation)
    assert isinstance(instance2, FooImplementation)
    assert instance1 is instance2
