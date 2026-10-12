from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pyrannic.contracts.database.query.builder import QueryBuilderInterface
    from pyrannic.contracts.database.query.expression import ExpressionInterface


class WhereClauseInterface(ABC):
    @property
    @abstractmethod
    def type(self) -> str:
        """Get the type of the WHERE clause."""

    @property
    @abstractmethod
    def query(self) -> "QueryBuilderInterface":
        """Get the query for a nested WHERE clause."""

    @property
    @abstractmethod
    def column(self) -> "str | ExpressionInterface":
        """Get the column for the WHERE clause."""

    @property
    @abstractmethod
    def value(self) -> "str | int | float | ExpressionInterface | None":
        """Get the value for the WHERE clause."""

    @property
    @abstractmethod
    def operator(self) -> str:
        """Get the operator for the WHERE clause."""

    @property
    @abstractmethod
    def boolean(self) -> str:
        """Get the boolean operator for the WHERE clause."""
