from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pyrannic.contracts.database.query.expression import ExpressionInterface


class AggregateClauseInterface(ABC):
    @property
    @abstractmethod
    def function(self) -> str:
        """Get the aggregate function name."""

    @property
    @abstractmethod
    def columns(self) -> list["str | ExpressionInterface"]:
        """Get the columns or expressions for the aggregate function."""
