import pytest

from pyrannic.contracts.container.container import ContainerInterface
from tests.unit.container.conftest import FooInterface, FooImplementation


def test_set_alias(container: ContainerInterface):
    container.set_alias(FooInterface, "foo")
    assert container.is_alias("foo")


def test_set_alias_itself(container: ContainerInterface):
    with pytest.raises(ValueError) as exc_info:
        container.set_alias(FooInterface, FooInterface)

    error = str(exc_info.value)
    assert f"{FooInterface} cannot be aliased to itself." in error


def test_set_alias_drop_stale_instances(container: ContainerInterface):
    container.set_alias(FooInterface, "foo")
    assert container.is_alias("foo")

    container.bind("foo", FooImplementation)  # type: ignore
    assert not container.is_alias("foo")
