from abc import ABC, abstractmethod
from typing import Any, Generic, Self, TypeVar, overload

from pyrannic.contracts.orm.model import ModelInterface

T = TypeVar("T", bound=ModelInterface)


class QueryBuilderInterface(ABC, Generic[T]):
    @property
    @abstractmethod
    def model(self) -> type[T]:
        """Return the model type associated with this query builder."""

    @abstractmethod
    def select(self, model: type[T] | None = None) -> Self:
        """Initialize a select query for the model."""

    @abstractmethod
    def delete(self, model: type[T] | None = None) -> Self:
        """Initialize a delete query for the model."""

    @abstractmethod
    def order_by(self, *attributes: Any) -> Self:
        """Set the order for the current query."""

    @abstractmethod
    def limit(self, limit: int | None) -> Self:
        """Set the limit for the current query."""

    @abstractmethod
    def offset(self, offset: int | None) -> Self:
        """Set the offset for the current query."""

    @overload
    @abstractmethod
    def where(self, *where_clause: Any) -> Self:
        """Add where conditions to the current query."""

    @overload
    @abstractmethod
    def where(self, **kwargs: Any) -> Self:
        """Add where conditions to the current query."""

    @abstractmethod
    def where_none(self, column_name: str) -> Self:
        """Add a where condition to check if the column is None."""

    @abstractmethod
    def where_not_none(self, column_name: str) -> Self:
        """Add a where condition to check if the column is not None."""

    @abstractmethod
    def filter(self, *filters: Any | None) -> Self:
        """Add filtering conditions to the current query."""

    @abstractmethod
    def filter_by(self, **kwargs: Any) -> Self:
        """Add filtering conditions to the current query."""

    @abstractmethod
    def group_by(self, *attributes: Any) -> Self:
        """Add group by conditions to the current query."""

    @abstractmethod
    def with_removed(self) -> Self:
        """Include removed records in the query results."""

    @abstractmethod
    def only_removed(self) -> Self:
        """Include only removed records in the query results."""
