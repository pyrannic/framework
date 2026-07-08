from abc import ABC, abstractmethod
from collections.abc import Callable
from typing import Any

from annotated_types import T
from fastapi import Request

from pyrannic.contracts.container.contextual_binding_builder import (
    ContextualBindingBuilderInterface,
)


class ContainerInterface(ABC):
    @abstractmethod
    def bind(
        self,
        abstract: str | type,
        concrete: type[Any] | Callable[..., Any],
        shared: bool = False,
    ) -> None:
        """Register a binding with the container."""
        pass

    @abstractmethod
    def bind_if(
        self,
        abstract: str | type,
        concrete: type[Any] | Callable[..., Any],
        shared: bool = False,
    ) -> None:
        """Register a binding if it hasn't already been registered."""
        pass

    @abstractmethod
    def scoped(
        self,
        abstract: str | type,
        concrete: type[Any] | Callable[..., Any],
    ) -> None:
        """Register a scoped binding in the container."""
        pass

    @abstractmethod
    def scoped_if(
        self,
        abstract: str | type,
        concrete: type[Any] | Callable[..., Any],
    ) -> None:
        """Register a scoped binding if it hasn't already been registered."""
        pass

    @abstractmethod
    def singleton(
        self,
        abstract: str | type,
        concrete: type[Any] | Callable[..., Any],
    ) -> None:
        """Register a shared binding in the container."""
        pass

    @abstractmethod
    def singleton_if(
        self,
        abstract: str | type,
        concrete: type[Any] | Callable[..., Any],
    ) -> None:
        """Register a shared binding if it hasn't already been registered."""
        pass

    @abstractmethod
    def instance(self, abstract: str | type[T], instance: T | None = None) -> T:
        """Register an existing instance as shared in the container or retrieve it from the container."""
        pass

    @abstractmethod
    def add_contextual_binding(
        self,
        concrete: type,
        abstract: str | type,
        implementation: type | Callable[..., Any],
    ) -> None:
        """Add a contextual binding to the container."""
        pass

    @abstractmethod
    def when(self, concrete: type | list[type]) -> ContextualBindingBuilderInterface:
        """Define a contextual binding."""
        pass

    @abstractmethod
    def is_bound(self, abstract: str | type) -> bool:
        """Determine if the given abstract type has been bound."""
        pass

    @abstractmethod
    async def resolve(
        self,
        abstract: str | type[T],
        request: Request | None = None,
    ) -> T:
        """Resolve the given type from the container."""
        pass

    @abstractmethod
    async def call(self, callback: type[T] | Callable[..., Any]) -> T:
        """Call the given callback (Closure, class@method...) and inject its dependencies."""
        pass

    @abstractmethod
    def resolved(self, abstract: str | type) -> bool:
        """Determine if the given abstract type has been resolved."""
        pass

    @abstractmethod
    def set_alias(self, abstract: str | type, alias: str | type) -> None:
        """Alias an abstract type to a different key or type."""
        pass

    @abstractmethod
    def is_alias(self, alias: str | type) -> bool:
        """Determine if a given key or type is an alias."""
        pass

    @abstractmethod
    def flush(self) -> None:
        """Flush the container of all bindings and resolved instances."""
        pass
