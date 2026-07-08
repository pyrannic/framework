from abc import ABC, abstractmethod
import asyncio
from typing import Annotated, Generator

from fastapi import Depends, Query, Request
import pytest

from pyrannic.container.decorators import scoped, singleton
from pyrannic.contracts.application import ApplicationInterface
from pyrannic.contracts.container.container import ContainerInterface
from pyrannic.ioc import Resolve


class FooInterface(ABC):
    @abstractmethod
    def foo_method(self) -> str:
        pass


class FooImplementation(FooInterface):
    def foo_method(self) -> str:
        return "FooImplementation"


class FooSecondaryImplementation(FooInterface):
    def foo_method(self) -> str:
        return "FooSecondaryImplementation"


class BarService:
    def __init__(self, foo_service: Resolve[FooInterface]):
        self.foo_service = foo_service


class BazService:
    def __init__(self, foo_service: Resolve[FooInterface]):
        self.foo_service = foo_service


@scoped
class ScopedClass(FooInterface):
    def foo_method(self) -> str:
        return "ScopedClass"


@singleton
class SingletonClass(FooInterface):
    def foo_method(self) -> str:
        return "SingletonClass"


def callable_with_dependencies(foo: Resolve[FooImplementation]) -> None:
    assert isinstance(foo, FooImplementation)
    assert foo.foo_method() == "FooImplementation"


def callable_with_dependencies_error(page: int) -> None:
    assert isinstance(page, int)


async def async_callable_with_dependencies(foo: Resolve[FooImplementation]) -> None:
    await asyncio.sleep(0.1)  # Simulate async work
    assert isinstance(foo, FooImplementation)
    assert foo.foo_method() == "FooImplementation"


async def resolve_foo_interface(
    app: ApplicationInterface,
    request: Request,
) -> FooInterface:
    await asyncio.sleep(0.1)  # Simulate async work
    return FooImplementation()


@pytest.fixture()
def container(
    application: ApplicationInterface,
) -> Generator[ContainerInterface, None, None]:
    yield application.container
    application.container.flush()
