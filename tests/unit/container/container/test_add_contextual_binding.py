import pytest

from pyrannic.container.container import Container
from tests.unit.container.conftest import BarService, FooImplementation, FooInterface


@pytest.mark.asyncio
async def test_add_contextual_binding(container: Container):
    container.add_contextual_binding(
        BarService,
        FooInterface,
        FooImplementation,
    )

    instance = await container.resolve(BarService)

    assert isinstance(instance.foo_service, FooImplementation)
    assert instance.foo_service.foo_method() == "FooImplementation"
