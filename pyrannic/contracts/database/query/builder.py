from abc import ABC, abstractmethod
from collections.abc import Callable
from typing import TYPE_CHECKING, Any, Self, overload

from pyrannic.contracts.database.query.clauses.order_by import (
    OrderByClauseInterface,
    SortDirection,
)
from pyrannic.contracts.database.query.clauses.where import WhereClauseInterface

if TYPE_CHECKING:
    from pyrannic.contracts.database.query.clauses.aggregate import (
        AggregateClauseInterface,
    )
    from pyrannic.contracts.database.query.expression import ExpressionInterface
    from pyrannic.contracts.database.query.grammar import GrammarInterface
    from pyrannic.contracts.database.query.join_builder import JoinBuilderInterface


class QueryBuilderInterface(ABC):
    @property
    @abstractmethod
    def grammar(self) -> "GrammarInterface":
        """Get the grammar instance associated with the query builder."""

    @property
    @abstractmethod
    def aggregate(self) -> "AggregateClauseInterface | None":
        """Get the aggregate function for the query."""

    @property
    @abstractmethod
    def columns(self) -> list["str | ExpressionInterface"]:
        """Get the list of columns selected for the query."""

    @property
    @abstractmethod
    def is_distinct(self) -> bool:
        """Check if the query is set to select distinct rows."""

    @property
    @abstractmethod
    def distinct_columns(self) -> list["str | ExpressionInterface"]:
        """Get the list of columns for which the query is set to select distinct rows."""

    @property
    @abstractmethod
    def from_clause(self) -> str:
        """Get the table specified for the query."""

    @property
    @abstractmethod
    def joins(self) -> list["JoinBuilderInterface"]:
        """Get the list of JOIN clauses for the query."""

    @property
    @abstractmethod
    def wheres(self) -> list[WhereClauseInterface]:
        """Get the list of WHERE conditions for the query."""

    @property
    @abstractmethod
    def groups(self) -> list["str | ExpressionInterface"]:
        """Get the list of GROUP BY clauses for the query."""

    @property
    @abstractmethod
    def orders(self) -> list[OrderByClauseInterface]:
        """Get the list of ORDER BY clauses."""

    @property
    @abstractmethod
    def limit_count(self) -> int | None:
        """Get the number of records to retrieve."""

    @property
    @abstractmethod
    def offset_count(self) -> int | None:
        """Get the number of records to skip in the query."""

    @abstractmethod
    def select(self, *columns: "str | ExpressionInterface") -> Self:
        """Select columns for the query."""

    @abstractmethod
    def select_raw(self, expression: str, *bindings: Any) -> Self:
        """Select raw columns for the query."""

    @abstractmethod
    def add_select(self, *column: "str | ExpressionInterface") -> Self:
        """Add a new select column to the query."""

    @abstractmethod
    def distinct(self, *columns: "str | ExpressionInterface") -> Self:
        """Set the query to select distinct rows."""

    @abstractmethod
    def set_aggregate(
        self,
        function: str,
        *columns: "str | ExpressionInterface",
    ) -> Self:
        """Set the aggregate function for the query."""

    @abstractmethod
    def from_(self, table: str, as_: str | None = None) -> Self:
        """Specify the table for the query."""

    @overload
    @abstractmethod
    def join(
        self,
        expression: "ExpressionInterface",
        callback: Callable[["JoinBuilderInterface"], None],
        /,
        *,
        type: str | None = None,
        where: bool = False,
    ) -> Self:
        """Add a JOIN clause to the query using a callback for the join condition."""

    @overload
    @abstractmethod
    def join(
        self,
        table: str,
        callback: Callable[["JoinBuilderInterface"], None],
        /,
        *,
        type: str | None = None,
        where: bool = False,
    ) -> Self:
        """Add a JOIN clause to the query using a callback for the join condition."""

    @overload
    @abstractmethod
    def join(
        self,
        table: str,
        left_operand: str,
        right_operand: str,
        /,
        *,
        type: str | None = None,
        where: bool = False,
    ) -> Self:
        """Add a JOIN clause to the query with a single ON condition."""

    @overload
    @abstractmethod
    def join(
        self,
        table: str,
        left_operand: str,
        operator: str | None = None,
        right_operand: str | None = None,
        /,
        *,
        type: str | None = None,
        where: bool = False,
    ) -> Self:
        """Add a JOIN clause to the query with optional ON conditions."""

    @abstractmethod
    def join(
        self,
        table_or_expression: "str | ExpressionInterface",
        left_operand: str
        | Callable[["JoinBuilderInterface"], "QueryBuilderInterface | None"]
        | None = None,
        operator: str | None = None,
        right_operand: str | None = None,
        /,
        *,
        type: str | None = None,
        where: bool = False,
    ) -> Self:
        """Add a JOIN clause to the query."""

    @overload
    @abstractmethod
    def join_lateral(self, query: "QueryBuilderInterface", /, as_: str) -> Self:
        """Add a LATERAL JOIN clause to the query."""

    @overload
    @abstractmethod
    def join_lateral(
        self,
        query: Callable[["QueryBuilderInterface"], "QueryBuilderInterface | None"],
        /,
        as_: str,
    ) -> Self:
        """Add a LATERAL JOIN clause to the query."""

    @abstractmethod
    def join_lateral(
        self,
        query: 'QueryBuilderInterface | Callable[["QueryBuilderInterface"], "QueryBuilderInterface | None"]',
        /,
        as_: str,
        type: str | None = None,
    ) -> Self:
        """Add a LATERAL JOIN clause to the query."""

    @overload
    @abstractmethod
    def join_sub(
        self,
        query: "QueryBuilderInterface",
        as_: str,
        callback: Callable[["JoinBuilderInterface"], "QueryBuilderInterface | None"],
        /,
        *,
        type: str | None = None,
        where: bool = False,
    ) -> Self:
        """Add a JOIN subquery to the query."""

    @overload
    @abstractmethod
    def join_sub(
        self,
        query: "QueryBuilderInterface",
        as_: str,
        first_column: "str | ExpressionInterface",
        operator: str | None = None,
        second_column: "str | ExpressionInterface | None" = None,
        /,
        *,
        type: str | None = None,
        where: bool = False,
    ) -> Self:
        """Add a JOIN subquery to the query."""

    @abstractmethod
    def join_sub(
        self,
        query: "QueryBuilderInterface",
        as_: str,
        first_column: 'str | ExpressionInterface | Callable[["JoinBuilderInterface"], "QueryBuilderInterface | None"]',
        operator: str | None = None,
        second_column: "str | ExpressionInterface | None" = None,
        /,
        *,
        type: str | None = None,
        where: bool = False,
    ) -> Self:
        """Add a JOIN subquery to the query."""

    @overload
    @abstractmethod
    def left_join_lateral(self, query: "QueryBuilderInterface", /, as_: str) -> Self:
        """Add a LEFT LATERAL JOIN clause to the query."""

    @overload
    @abstractmethod
    def left_join_lateral(
        self,
        query: Callable[["QueryBuilderInterface"], "QueryBuilderInterface | None"],
        /,
        as_: str,
    ) -> Self:
        """Add a LEFT LATERAL JOIN clause to the query."""

    @abstractmethod
    def left_join_lateral(
        self,
        query: 'QueryBuilderInterface | Callable[["QueryBuilderInterface"], "QueryBuilderInterface | None"]',
        /,
        as_: str,
    ) -> Self:
        """Add a LEFT LATERAL JOIN clause to the query."""

    @overload
    @abstractmethod
    def left_join(
        self,
        expression: "ExpressionInterface",
        callback: Callable[["JoinBuilderInterface"], "QueryBuilderInterface | None"],
        /,
    ) -> Self:
        """Add a LEFT JOIN clause to the query using a callback for the join condition."""

    @overload
    @abstractmethod
    def left_join(
        self,
        table: str,
        callback: Callable[["JoinBuilderInterface"], "QueryBuilderInterface | None"],
        /,
    ) -> Self:
        """Add a LEFT JOIN clause to the query using a callback for the join condition."""

    @overload
    @abstractmethod
    def left_join(
        self,
        table: str,
        left_operand: str,
        right_operand: str,
        /,
    ) -> Self:
        """Add a LEFT JOIN clause to the query."""

    @overload
    @abstractmethod
    def left_join(
        self,
        table: str,
        left_operand: str,
        operator: str | None = None,
        right_operand: str | None = None,
        /,
    ) -> Self:
        """Add a LEFT JOIN clause to the query."""

    @abstractmethod
    def left_join(
        self,
        table_or_expression: "str | ExpressionInterface",
        left_operand: str
        | Callable[["JoinBuilderInterface"], "QueryBuilderInterface | None"]
        | None = None,
        operator: str | None = None,
        right_operand: str | None = None,
        /,
    ) -> Self:
        """Add a LEFT JOIN clause to the query."""

    @overload
    @abstractmethod
    def left_join_sub(
        self,
        query: "QueryBuilderInterface",
        as_: str,
        callback: Callable[["JoinBuilderInterface"], "QueryBuilderInterface | None"],
        /,
    ) -> Self:
        """Add a LEFT JOIN subquery to the query."""

    @overload
    @abstractmethod
    def left_join_sub(
        self,
        query: "QueryBuilderInterface",
        as_: str,
        first_column: "str | ExpressionInterface",
        operator: str | None = None,
        second_column: "str | ExpressionInterface | None" = None,
        /,
    ) -> Self:
        """Add a LEFT JOIN subquery to the query."""

    @abstractmethod
    def left_join_sub(
        self,
        query: "QueryBuilderInterface",
        as_: str,
        first_column: 'str | ExpressionInterface | Callable[["JoinBuilderInterface"], "QueryBuilderInterface | None"]',
        operator: str | None = None,
        second_column: "str | ExpressionInterface | None" = None,
        /,
    ) -> Self:
        """Add a LEFT JOIN subquery to the query."""

    @overload
    @abstractmethod
    def where(
        self,
        callback: Callable[["QueryBuilderInterface"], "QueryBuilderInterface | None"],
        /,
        *,
        boolean: str = "and",
    ) -> Self:
        """Add a nested WHERE condition to the query."""

    @overload
    @abstractmethod
    def where(
        self,
        column: "str | ExpressionInterface",
        value: Any,
        /,
        *,
        boolean: str = "and",
    ) -> Self:
        """A simple WHERE condition with a column and value."""

    @overload
    @abstractmethod
    def where(
        self,
        column: "str | ExpressionInterface",
        operator: str,
        value: Any,
        /,
        *,
        boolean: str = "and",
    ) -> Self:
        """A simple WHERE condition with a column, operator, and value."""

    @abstractmethod
    def where(
        self,
        column: 'str | ExpressionInterface | Callable[["QueryBuilderInterface"], "QueryBuilderInterface | None"]',
        operator: str | None = None,
        value: Any = None,
        /,
        *,
        boolean: str = "and",
    ) -> Self:
        """Add a WHERE condition to the query."""

    @overload
    @abstractmethod
    def or_where(
        self,
        callback: Callable[["QueryBuilderInterface"], "QueryBuilderInterface | None"],
        /,
    ) -> Self:
        """Add a nested OR WHERE condition to the query."""

    @overload
    @abstractmethod
    def or_where(
        self,
        column: "str | ExpressionInterface",
        value: Any,
        /,
    ) -> Self:
        """Add an OR WHERE condition to the query."""

    @overload
    @abstractmethod
    def or_where(
        self,
        column: "str | ExpressionInterface",
        operator: str,
        value: Any,
        /,
    ) -> Self:
        """Add an OR WHERE condition to the query."""

    @abstractmethod
    def or_where(
        self,
        column: 'str | ExpressionInterface | Callable[["QueryBuilderInterface"], "QueryBuilderInterface | None"]',
        operator: str | None = None,
        value: Any = None,
        /,
    ) -> Self:
        """Add an OR WHERE condition to the query."""

    @overload
    @abstractmethod
    def where_column(
        self,
        left_column: str,
        right_column: str,
        /,
    ) -> Self:
        """Add a WHERE condition comparing two columns."""

    @overload
    @abstractmethod
    def where_column(
        self,
        left_column: str,
        operator: str,
        right_column: str,
        /,
    ) -> Self:
        """Add a WHERE condition comparing two columns."""

    @abstractmethod
    def where_column(
        self,
        left_column: str,
        operator: str | None = None,
        right_column: str | None = None,
        /,
        boolean: str = "and",
    ) -> Self:
        """Add a WHERE condition comparing two columns."""

    @abstractmethod
    def where_null(
        self,
        *columns: "str | ExpressionInterface",
        boolean: str = "and",
        not_: bool = False,
    ) -> Self:
        """Add a WHERE NULL condition to the query."""

    @abstractmethod
    def where_not_null(
        self,
        *columns: "str | ExpressionInterface",
        boolean: str = "and",
    ) -> Self:
        """Add a WHERE NOT NULL condition to the query."""

    @abstractmethod
    def where_in(
        self,
        column: "str | ExpressionInterface",
        values: list[Any],
        /,
        *,
        boolean: str = "and",
        not_: bool = False,
    ) -> Self:
        """Add an WHERE IN condition to the query."""

    @abstractmethod
    def or_where_in(
        self,
        column: "str | ExpressionInterface",
        values: list[Any],
        /,
    ) -> Self:
        """Add an OR WHERE IN condition to the query."""

    @abstractmethod
    def where_not_in(
        self,
        column: "str | ExpressionInterface",
        values: list[Any],
        /,
        *,
        boolean: str = "and",
    ) -> Self:
        """Add a WHERE NOT IN condition to the query."""

    @abstractmethod
    def or_where_not_in(
        self,
        column: "str | ExpressionInterface",
        values: list[Any],
        /,
    ) -> Self:
        """Add an OR WHERE NOT IN condition to the query."""

    @abstractmethod
    def where_nested(
        self,
        callback: "Callable[[QueryBuilderInterface], QueryBuilderInterface | None]",
        /,
        *,
        boolean: str = "and",
    ) -> Self:
        """Add a nested WHERE condition to the query."""

    @abstractmethod
    def group_by(self, *columns: "str | ExpressionInterface") -> Self:
        """Add a GROUP BY clause to the query based on the specified columns."""

    @abstractmethod
    def group_by_raw(self, expression: str, *bindings: Any) -> Self:
        """Add a GROUP BY clause using a raw expression."""

    @abstractmethod
    def order_by(
        self,
        column: "str | ExpressionInterface",
        direction: SortDirection = SortDirection.ASC,
        /,
    ) -> Self:
        """Add an ORDER BY clause to sort the results based on the specified column."""

    @abstractmethod
    def order_by_asc(self, column: "str | ExpressionInterface", /) -> Self:
        """Add an ORDER BY clause to sort the results in ascending order based on the specified column."""

    @abstractmethod
    def order_by_desc(self, column: "str | ExpressionInterface", /) -> Self:
        """Add an ORDER BY clause to sort the results in descending order based on the specified column."""

    @abstractmethod
    def order_by_raw(self, expression: str, *bindings: Any) -> Self:
        """Add an ORDER BY clause using a raw expression."""

    @abstractmethod
    def latest(self, column: str = "created_at", /) -> Self:
        """Add an ORDER BY clause to get the latest record based on the specified column."""

    @abstractmethod
    def oldest(self, column: str = "created_at", /) -> Self:
        """Add an ORDER BY clause to get the oldest record based on the specified column."""

    @abstractmethod
    def skip(self, amount: int, /) -> Self:
        """Skip a specified number of records in the query."""

    @abstractmethod
    def offset(self, amount: int, /) -> Self:
        """Skip a specified number of records in the query."""

    @abstractmethod
    def take(self, amount: int, /) -> Self:
        """Limit the query to a specified number of records."""

    @abstractmethod
    def limit(self, amount: int, /) -> Self:
        """Limit the query to a specified number of records."""

    @abstractmethod
    def to_sql(self) -> str:
        """Convert the query to its SQL representation."""

    @abstractmethod
    def to_raw_sql(self) -> str:
        """Get the raw SQL representation of the query with embedded bindings."""

    @abstractmethod
    def raw(self, value: str | float, /) -> "ExpressionInterface":
        """Create a raw database expression."""

    @abstractmethod
    def get_bindings(self) -> list[Any]:
        """Get the list of all bindings for the query."""

    @abstractmethod
    def add_binding(self, *value: Any, type: str = "where") -> None:
        """Add a binding value for the query of the specified type."""

    @abstractmethod
    def clone(self) -> Self:
        """Create a clone of the current query builder instance."""

    @overload
    @abstractmethod
    def clone_without(self, *attributes: str) -> Self:
        """Clone the query builder without the specified attributes."""

    @overload
    @abstractmethod
    def clone_without(
        self,
        *,
        attributes: list[str],
        bindings: list[str],
    ) -> Self:
        """Clone the query builder without the specified attributes and bindings."""

    @abstractmethod
    def clone_without(
        self,
        *args: str,
        attributes: list[str] | None = None,
        bindings: list[str] | None = None,
    ) -> Self:
        """Clone the query builder without the specified attributes and bindings."""
