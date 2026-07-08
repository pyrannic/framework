from fastapi.exceptions import ValidationException
import pytest

from pyrannic.contracts.container.container import ContainerInterface
from tests.unit.container.conftest import (
    FooImplementation,
    callable_with_dependencies,
    async_callable_with_dependencies,
    callable_with_dependencies_error,
)


@pytest.mark.asyncio
async def test_call_with_callable(container: ContainerInterface):
    await container.call(callable_with_dependencies)


@pytest.mark.asyncio
async def test_call_with_callable_error(container: ContainerInterface):
    with pytest.raises(ValidationException) as exc_info:
        await container.call(callable_with_dependencies_error)

    error = str(exc_info.value)
    assert "1 validation error:" in error
    assert "'loc': ('query', 'page')" in error
    assert "Field required" in error


@pytest.mark.asyncio
async def test_call_with_async_callable(container: ContainerInterface):
    await container.call(async_callable_with_dependencies)


@pytest.mark.asyncio
async def test_call_with_class(container: ContainerInterface):
    instance = await container.call(FooImplementation)
    assert isinstance(instance, FooImplementation)
    assert instance.foo_method() == "FooImplementation"
