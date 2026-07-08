from typing import Any, Callable, Self

from pyrannic.contracts.container.container import ContainerInterface
from pyrannic.contracts.container.contextual_binding_builder import (
    ContextualBindingBuilderInterface,
)


class ContextualBindingBuilder(ContextualBindingBuilderInterface):
    def __init__(
        self,
        container: ContainerInterface,
        concrete: type | list[type],
    ) -> None:
        self._container = container
        self._concrete = concrete

    def needs(self, abstract: str | type) -> Self:
        self._needs = abstract
        return self

    def give(self, implementation: type | Callable[..., Any]) -> Self:
        concretes = (
            [self._concrete] if not isinstance(self._concrete, list) else self._concrete
        )

        for concrete in concretes:
            self._container.add_contextual_binding(
                concrete, self._needs, implementation
            )

        return self
