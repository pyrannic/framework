from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pyrannic.contracts.database.query.builder import QueryBuilderInterface


class SetClauseInterface(ABC):
    @property
    @abstractmethod
    def type(self) -> str:
        """Get the set type. E.g., UNION, INTERSECT, EXCEPT"""

    @property
    @abstractmethod
    def query(self) -> "QueryBuilderInterface":
        """Get the query for this set clause."""
