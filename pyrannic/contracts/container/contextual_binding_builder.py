from abc import ABC, abstractmethod
from typing import Any, Callable, Self


class ContextualBindingBuilderInterface(ABC):
    @abstractmethod
    def needs(self, abstract: str | type) -> Self:
        """Define the abstract target that depends on the context."""
        pass

    @abstractmethod
    def give(self, implementation: type | Callable[..., Any]) -> Self:
        """Define the implementation for the contextual binding."""
        pass
