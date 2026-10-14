from collections.abc import Callable
from typing import Any, Self, overload

from pyrannic.contracts.database import (
    GrammarInterface,
    OrderByClauseInterface,
    QueryBuilderInterface,
    SortDirection,
    WhereClauseInterface,
)
from pyrannic.contracts.database.query.expression import ExpressionInterface
from pyrannic.contracts.database.query.join_builder import JoinBuilderInterface
from pyrannic.database.query.clauses import OrderByClause, WhereClause
from pyrannic.database.query.expression import Expression
from pyrannic.ioc import Resolves
from pyrannic.support.collections import li
from pyrannic.support.collections.dict import flatten


class QueryBuilder(QueryBuilderInterface):
    _columns: list[str | ExpressionInterface]
    """List of columns to be selected."""

    _distinct = False
    """Indicates whether the query should select distinct results."""

    _grammar: GrammarInterface
    """Grammar interface for building SQL queries."""

    _from: str
    """Table specified for the query."""

    _joins: list[JoinBuilderInterface]
    """List of JOIN clauses."""

    _wheres: list[WhereClauseInterface]
    """List of WHERE conditions."""

    _groups: list[str | ExpressionInterface]
    """List of GROUP BY clauses."""

    _orders: list[OrderByClauseInterface]
    """List of ORDER BY clauses."""

    _limit: int | None
    """Limit for the number of records to retrieve."""

    _offset: int | None
    """Number of records to skip in the query."""

    _bindings: dict[str, list[Any]]
    """Bindings for query parameters."""

    _operators: list[str]
    """List of valid SQL operators."""

    def __init__(self, grammar: Resolves[GrammarInterface]) -> None:
        self._grammar = grammar
        self._reset()

    def _reset(self) -> None:
        self._operators = [
            "=",
            "<",
            ">",
            "<=",
            ">=",
            "<>",
            "!=",
            "<=>",
            "like",
            "like binary",
            "not like",
            "ilike",
            "&",
            "|",
            "^",
            "<<",
            ">>",
            "&~",
            "is",
            "is not",
            "rlike",
            "not rlike",
            "regexp",
            "not regexp",
            "~",
            "~*",
            "!~",
            "!~*",
            "similar to",
            "not similar to",
            "not ilike",
            "~~*",
            "!~~*",
        ]
        self._bindings = {
            "select": [],
            "from": [],
            "join": [],
            "where": [],
            "group_by": [],
            "having": [],
            "order_by": [],
            "union": [],
            "unionOrder": [],
        }
        self._distinct = False
        self._columns = []
        self._from = ""
        self._joins = []
        self._wheres = []
        self._groups = []
        self._orders = []
        self._limit = None
        self._offset = None

    @property
    def grammar(self) -> GrammarInterface:
        return self._grammar

    @property
    def columns(self) -> list[str | ExpressionInterface]:
        return self._columns

    @property
    def is_distinct(self) -> bool:
        return self._distinct

    @property
    def from_clause(self) -> str:
        return self._from

    @property
    def joins(self) -> list[JoinBuilderInterface]:
        return self._joins

    @property
    def wheres(self) -> list[WhereClauseInterface]:
        return self._wheres

    @property
    def groups(self) -> list[str | ExpressionInterface]:
        return self._groups

    @property
    def orders(self) -> list[OrderByClauseInterface]:
        return self._orders

    @property
    def limit_count(self) -> int | None:
        return self._limit

    @property
    def offset_count(self) -> int | None:
        return self._offset

    def select(self, *columns: str | ExpressionInterface) -> Self:
        self._columns = list(columns or ["*"])
        return self

    def select_raw(self, expression: str, *bindings: Any) -> Self:
        self.add_select(self.raw(expression))

        if bindings:
            self.add_binding(*bindings, type="select")

        return self

    def add_select(self, *column: str | ExpressionInterface) -> Self:
        for col in column:
            if col not in self._columns:
                self._columns.append(col)

        return self

    def distinct(self) -> Self:
        self._distinct = True
        return self

    def from_(self, table: str, as_: str | None = None) -> Self:
        self._from = f"{table} as {as_}" if as_ else table
        return self

    @overload
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

    def join(
        self,
        table_or_expression: str | ExpressionInterface,
        left_operand: str | Callable[[JoinBuilderInterface], None] | None = None,
        operator: str | None = None,
        right_operand: str | None = None,
        /,
        *,
        type: str | None = None,
        where: bool = False,
    ) -> Self:
        from pyrannic.database.query.join_builder import JoinBuilder

        join_builder = JoinBuilder(self, type or "inner", table_or_expression)

        if callable(left_operand):
            left_operand(join_builder)
            self._joins.append(join_builder)
        else:
            method = getattr(join_builder, "where" if where else "on")
            self._joins.append(method(left_operand, operator, right_operand))

        self.add_binding(*join_builder.get_bindings(), type="join")

        return self

    @overload
    def where(
        self,
        callback: Callable[[QueryBuilderInterface], QueryBuilderInterface | None],
        /,
        *,
        boolean: str = "and",
    ) -> Self:
        """Add a nested WHERE condition to the query."""

    @overload
    def where(
        self,
        column: str | ExpressionInterface,
        value: Any,
        /,
        *,
        boolean: str = "and",
    ) -> Self:
        """Add a basic WHERE clause with a column and value."""

    @overload
    def where(
        self,
        column: str | ExpressionInterface,
        operator: str,
        value: Any,
        /,
        *,
        boolean: str = "and",
    ) -> Self:
        """Add a basic WHERE clause with a column, operator, and value."""

    def where(
        self,
        column: str
        | ExpressionInterface
        | Callable[[QueryBuilderInterface], QueryBuilderInterface | None],
        operator: str | None = None,
        value: Any = None,
        /,
        *,
        boolean: str = "and",
    ) -> Self:
        if callable(column):
            return self.where_nested(column, boolean=boolean)

        where_type = "basic"

        if operator is None and value is None:
            value = None
            operator = "="
        elif value is None:
            value = operator
            operator = "="
        else:
            operator = operator or "="

        self._wheres.append(WhereClause(column, operator, value, boolean, where_type))
        self.add_binding(li.flatten([value]), type="where")

        return self

    @overload
    def or_where(
        self,
        callback: Callable[[QueryBuilderInterface], QueryBuilderInterface | None],
        /,
    ) -> Self:
        """Add a nested OR WHERE condition to the query."""

    @overload
    def or_where(
        self,
        column: str | ExpressionInterface,
        value: Any,
        /,
    ) -> Self:
        """Add an OR WHERE condition to the query."""

    @overload
    def or_where(
        self,
        column: str | ExpressionInterface,
        operator: str,
        value: Any,
        /,
    ) -> Self:
        """Add an OR WHERE condition to the query."""

    def or_where(
        self,
        column: str
        | ExpressionInterface
        | Callable[[QueryBuilderInterface], QueryBuilderInterface | None],
        operator: str | None = None,
        value: Any = None,
        /,
    ) -> Self:
        if callable(column):
            return self.where(column, boolean="or")

        if value is None:
            return self.where(column, operator, boolean="or")

        return self.where(column, operator or "=", value, boolean="or")

    def where_column(
        self,
        left_column: str | ExpressionInterface,
        operator: str | None = None,
        right_column: str | ExpressionInterface | None = None,
        /,
        boolean: str = "and",
    ) -> Self:
        if not self._is_valid_operator(operator):
            right_column = operator
            operator = "="

        self._wheres.append(
            WhereClause(left_column, operator or "=", right_column, boolean, "column")
        )

        return self

    def where_nested(
        self,
        callback: Callable[[QueryBuilderInterface], QueryBuilderInterface | None],
        /,
        *,
        boolean: str = "and",
    ) -> Self:
        query = self._query_for_nested_where()
        callback(query)

        return self._add_nested_where(query, boolean)

    def _add_nested_where(self, query: Self, boolean: str) -> Self:
        if not query.wheres:
            return self

        self._wheres.append(WhereClause.nested(query, boolean))

        self.add_binding(*query.get_raw_bindings()["where"], type="where")

        return self

    def _new_query(self) -> Self:
        return type(self)(self.grammar)

    def _query_for_nested_where(self) -> Self:
        return self._new_query().from_(self._from)

    def group_by(self, *columns: "str | ExpressionInterface") -> Self:
        self._groups.extend(columns)
        return self

    def group_by_raw(self, expression: str, *bindings: Any) -> Self:
        self._groups.append(self.raw(expression))
        self.add_binding(*bindings, type="group_by")

        return self

    def order_by(
        self,
        column: str | ExpressionInterface,
        direction: SortDirection = SortDirection.ASC,
        /,
    ) -> Self:
        self._orders.append(OrderByClause(column, direction))
        return self

    def order_by_asc(self, column: str | ExpressionInterface, /) -> Self:
        self.order_by(column, SortDirection.ASC)
        return self

    def order_by_desc(self, column: str | ExpressionInterface, /) -> Self:
        self.order_by(column, SortDirection.DESC)
        return self

    def order_by_raw(self, expression: str, *bindings: Any) -> Self:
        self._orders.append(OrderByClause(self.raw(expression)))
        self.add_binding(*bindings, type="order_by")
        return self

    def latest(self, column: str = "created_at", /) -> Self:
        self.order_by(column, SortDirection.DESC)
        return self

    def oldest(self, column: str = "created_at", /) -> Self:
        self.order_by(column, SortDirection.ASC)
        return self

    def skip(self, amount: int, /) -> Self:
        return self.offset(amount)

    def offset(self, amount: int, /) -> Self:
        self._offset = amount
        return self

    def take(self, amount: int, /) -> Self:
        return self.limit(amount)

    def limit(self, amount: int, /) -> Self:
        self._limit = amount
        return self

    def to_sql(self) -> str:
        return self.grammar.compile_select(self)

    def to_raw_sql(self) -> str:
        return self.grammar.substitute_bindings_into_raw_sql(
            self.to_sql(),
            self.get_bindings(),
        )

    def raw(self, value: str | float, /) -> ExpressionInterface:
        return Expression(value)

    def get_bindings(self) -> list[Any]:
        return flatten(self._bindings)

    def get_raw_bindings(self) -> dict[str, list[Any]]:
        return self._bindings

    def add_binding(self, *value: Any, type: str = "where") -> None:
        if type not in self._bindings:
            raise ValueError(f"Invalid binding type: '{type}'")

        if not value:
            return

        self._bindings[type].extend(value)

    def _is_valid_operator(self, operator: str | None, /) -> bool:
        return isinstance(operator, str) and (
            operator in self.grammar.operators or operator in self._operators
        )

    def get(self) -> list[Any]:
        return self._process_select(self, self._run_select())

    def _process_select(
        self,
        builder: QueryBuilderInterface,
        results: list[Any],
        /,
    ) -> list[Any]:
        # TODO
        raise NotImplementedError()  # pragma: no cover

    def _run_select(self) -> list[Any]:
        # TODO
        raise NotImplementedError()  # pragma: no cover
