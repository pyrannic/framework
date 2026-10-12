from abc import ABC, abstractmethod
from enum import Enum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pyrannic.contracts.database.query.expression import ExpressionInterface


class SortDirection(Enum):
    ASC = "asc"
    DESC = "desc"


class OrderByClauseInterface(ABC):
    @property
    @abstractmethod
    def is_raw(self) -> bool:
        """Determine if the ORDER BY clause is a raw expression."""

    @property
    @abstractmethod
    def expression(self) -> "ExpressionInterface | None":
        """Get the raw expression for the ORDER BY clause."""

    @property
    @abstractmethod
    def column(self) -> str | None:
        """Get the column for the ORDER BY clause."""

    @property
    @abstractmethod
    def direction(self) -> SortDirection:
        """Get the sort direction for the ORDER BY clause."""
