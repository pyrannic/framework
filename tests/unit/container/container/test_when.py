import pytest

from pyrannic.container.container import Container
from pyrannic.container.contextual_binding_builder import ContextualBindingBuilder
from tests.unit.container.conftest import (
    BarService,
    BazService,
    FooInterface,
    FooSecondaryImplementation,
)


def test_when_with_single_value(container: Container):
    builder = container.when(BarService)

    assert isinstance(builder, ContextualBindingBuilder)


def test_when_with_list(container: Container):
    builder = container.when([BarService, BazService])

    assert isinstance(builder, ContextualBindingBuilder)


@pytest.mark.asyncio
async def test_contextual_binding(container: Container):
    container.when(BarService).needs(FooInterface).give(FooSecondaryImplementation)

    instance = await container.resolve(BarService)

    assert isinstance(instance.foo_service, FooSecondaryImplementation)
    assert instance.foo_service.foo_method() == "FooSecondaryImplementation"
