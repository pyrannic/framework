from abc import ABC, abstractmethod

from pyrannic.contracts.orm.query_builder import QueryBuilderInterface


class ScopeInterface[T](ABC):
    """
    Interface for defining query scopes that can be applied to query builders.
    """

    @abstractmethod
    def apply(self, repository: QueryBuilderInterface[T]) -> None:
        """
        Apply the scope to the given query builder.
        """
