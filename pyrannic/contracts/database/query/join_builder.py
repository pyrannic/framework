from abc import abstractmethod
from typing import TYPE_CHECKING, Self, overload

from pyrannic.contracts.database.query.builder import QueryBuilderInterface

if TYPE_CHECKING:
    from pyrannic.contracts.database.query.expression import ExpressionInterface
    from pyrannic.contracts.database.query.grammar import GrammarInterface


class JoinBuilderInterface(QueryBuilderInterface):
    @property
    @abstractmethod
    def type(self) -> str:
        """Get the type of the JOIN clause."""

    @property
    @abstractmethod
    def table(self) -> "str | ExpressionInterface":
        """Get the table for the JOIN clause."""

    @property
    @abstractmethod
    def parent_grammar(self) -> "GrammarInterface":
        """Get the grammar instance associated with the query builder."""

    @overload
    @abstractmethod
    def on(
        self,
        left_operand: "str | ExpressionInterface",
        right_operand: "str | ExpressionInterface",
        /,
    ) -> Self:
        """Add an ON clause to the JOIN statement."""

    @overload
    @abstractmethod
    def on(
        self,
        left_operand: "str | ExpressionInterface",
        operator: str,
        right_operand: "str | ExpressionInterface",
        /,
    ) -> Self:
        """Add an ON clause to the JOIN statement."""

    @abstractmethod
    def on(
        self,
        left_operand: "str | ExpressionInterface",
        operator: "str | ExpressionInterface | None" = None,
        right_operand: "str | ExpressionInterface | None" = None,
        /,
        boolean: str = "and",
    ) -> Self:
        """Add an ON clause to the JOIN statement."""

    @overload
    @abstractmethod
    def or_on(
        self,
        left_operand: "str | ExpressionInterface",
        right_operand: "str | ExpressionInterface",
        /,
    ) -> Self:
        """Add an OR ON clause to the JOIN statement."""

    @overload
    @abstractmethod
    def or_on(
        self,
        left_operand: "str | ExpressionInterface",
        operator: str,
        right_operand: "str | ExpressionInterface",
        /,
    ) -> Self:
        """Add an OR ON clause to the JOIN statement."""

    @abstractmethod
    def or_on(
        self,
        left_operand: "str | ExpressionInterface",
        operator: "str | ExpressionInterface | None" = None,
        right_operand: "str | ExpressionInterface | None" = None,
        /,
    ) -> Self:
        """Add an OR ON clause to the JOIN statement."""
