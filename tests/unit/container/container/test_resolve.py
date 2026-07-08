from fastapi.exceptions import RequestValidationError
import pytest

from pyrannic.contracts.container.container import ContainerInterface
from tests.unit.container.conftest import FooInterface, FooSecondaryImplementation


@pytest.mark.asyncio
async def test_resolve_concrete_class(container: ContainerInterface):
    instance = await container.resolve(FooSecondaryImplementation)

    assert not container.is_bound(FooSecondaryImplementation)
    assert isinstance(instance, FooSecondaryImplementation)


@pytest.mark.asyncio
async def test_resolve_with_interface_not_bound(container: ContainerInterface):
    with pytest.raises(RequestValidationError) as exc_info:
        await container.resolve(FooInterface)

    error = str(exc_info.value)
    print(error)
    assert "No binding found for interface FooInterface" in error


@pytest.mark.asyncio
async def test_resolve_with_key_not_bound(container: ContainerInterface):
    with pytest.raises(RequestValidationError) as exc_info:
        await container.resolve("FooInterface")

    error = str(exc_info.value)
    print(error)
    assert "No binding found for key FooInterface" in error
