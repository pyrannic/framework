import pytest

from pyrannic.contracts.container.container import ContainerInterface
from tests.unit.container.conftest import FooImplementation


@pytest.mark.asyncio
async def test_resolved_with_class(container: ContainerInterface):
    instance = await container.resolve(FooImplementation)
    assert isinstance(instance, FooImplementation)
    assert instance.foo_method() == "FooImplementation"
    assert container.resolved(FooImplementation)


@pytest.mark.asyncio
async def test_resolved_with_key(container: ContainerInterface):
    container.singleton("FooImplementation", FooImplementation)
    instance: FooImplementation = await container.resolve("FooImplementation")
    assert isinstance(instance, FooImplementation)
    assert instance.foo_method() == "FooImplementation"
    assert container.resolved("FooImplementation")
