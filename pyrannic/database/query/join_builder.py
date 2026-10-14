from typing import Self, overload

from pyrannic.contracts.database import (
    ExpressionInterface,
    GrammarInterface,
    JoinBuilderInterface,
    QueryBuilderInterface,
)
from pyrannic.database.query.builder import QueryBuilder


class JoinBuilder(QueryBuilder, JoinBuilderInterface):
    _type: str
    _table: str | ExpressionInterface

    def __init__(
        self,
        parent_query: QueryBuilderInterface,
        type: str,
        table: str | ExpressionInterface,
        /,
    ) -> None:
        super().__init__(parent_query.grammar)
        self._type = type
        self._table = table

    @property
    def type(self) -> str:
        return self._type

    @property
    def table(self) -> str | ExpressionInterface:
        return self._table

    @property
    def parent_grammar(self) -> GrammarInterface:
        return self._grammar

    @overload
    def on(
        self,
        left_operand: str | ExpressionInterface,
        right_operand: str | ExpressionInterface,
        /,
        *,
        boolean: str = "and",
    ) -> Self:
        """Add an ON clause to the JOIN statement."""

    @overload
    def on(
        self,
        left_operand: str | ExpressionInterface,
        operator: str,
        right_operand: str | ExpressionInterface,
        /,
        *,
        boolean: str = "and",
    ) -> Self:
        """Add an ON clause to the JOIN statement."""

    def on(
        self,
        left_operand: str | ExpressionInterface,
        operator: str | ExpressionInterface | None = None,
        right_operand: str | ExpressionInterface | None = None,
        /,
        boolean: str = "and",
    ) -> Self:
        if right_operand is None:
            right_operand = operator
            operator = "="

        assert isinstance(operator, str)

        return self.where_column(left_operand, operator, right_operand, boolean=boolean)

    @overload
    def or_on(
        self,
        left_operand: str | ExpressionInterface,
        right_operand: str | ExpressionInterface,
        /,
    ) -> Self:
        """Add an OR ON clause to the JOIN statement."""

    @overload
    def or_on(
        self,
        left_operand: str | ExpressionInterface,
        operator: str,
        right_operand: str | ExpressionInterface,
        /,
    ) -> Self:
        """Add an OR ON clause to the JOIN statement."""

    def or_on(
        self,
        left_operand: str | ExpressionInterface,
        operator: str | ExpressionInterface | None = None,
        right_operand: str | ExpressionInterface | None = None,
        /,
    ) -> Self:
        if operator and right_operand is None:
            return self.on(left_operand, operator, boolean="or")
        elif isinstance(operator, str) and right_operand:
            return self.on(left_operand, operator, right_operand, boolean="or")

        return self  # pragma: no cover
