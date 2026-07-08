from abc import ABC, abstractmethod
from typing import Generic

from pyrannic.contracts.orm.query_builder import QueryBuilderInterface, T


class ScopeInterface(ABC, Generic[T]):
    """
    Interface for defining query scopes that can be applied to query builders.
    """

    @abstractmethod
    def apply(self, repository: QueryBuilderInterface[T]) -> None:
        """
        Apply the scope to the given query builder.
        """
        pass
