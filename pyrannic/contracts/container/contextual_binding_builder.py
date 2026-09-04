from abc import ABC, abstractmethod
from collections.abc import Callable
from typing import Any, Self


class ContextualBindingBuilderInterface(ABC):
    @abstractmethod
    def needs(self, abstract: str | type) -> Self:
        """Define the abstract target that depends on the context."""

    @abstractmethod
    def give(self, implementation: type | Callable[..., Any]) -> Self:
        """Define the implementation for the contextual binding."""
