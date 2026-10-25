from collections.abc import Callable
from typing import Any, Self, overload

from pyrannic.contracts.database import (
    AggregateClauseInterface,
    GrammarInterface,
    OrderByClauseInterface,
    QueryBuilderInterface,
    SortDirection,
    WhereClauseInterface,
)
from pyrannic.contracts.database.query.expression import ExpressionInterface
from pyrannic.contracts.database.query.join_builder import JoinBuilderInterface
from pyrannic.database.query.clauses import OrderByClause, WhereClause
from pyrannic.database.query.clauses.aggregate import AggregateClause
from pyrannic.database.query.expression import Expression
from pyrannic.ioc import Resolves
from pyrannic.support.collections import li
from pyrannic.support.collections.dict import flatten


class QueryBuilder(QueryBuilderInterface):
    _aggregate: AggregateClauseInterface | None
    """Aggregate functions to be applied."""

    _ctes: list[str]
    """List of CTEs (Common Table Expressions) to be specified in the query."""

    _columns: list[str | ExpressionInterface]
    """List of columns to be selected."""

    _distinct: list[str | ExpressionInterface]
    """List of columns for which the query should select distinct results."""

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
            "with": [],
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
        self._ctes = []
        self._distinct = []
        self._aggregate = None
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
    def aggregate(self) -> AggregateClauseInterface | None:
        return self._aggregate

    @property
    def ctes(self) -> list[str]:
        return self._ctes

    @property
    def columns(self) -> list[str | ExpressionInterface]:
        return self._columns

    @property
    def is_distinct(self) -> bool:
        return len(self._distinct) > 0

    @property
    def distinct_columns(self) -> list[str | ExpressionInterface]:
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

    @overload
    def select_subquery(self, query: QueryBuilderInterface, as_: str, /) -> Self:
        """Add a new select column as a subquery to the query."""

    @overload
    def select_subquery(
        self,
        callback: Callable[[QueryBuilderInterface], QueryBuilderInterface | None],
        as_: str,
        /,
    ) -> Self:
        """Add a new select column as a subquery to the query."""

    def select_subquery(
        self,
        query: QueryBuilderInterface
        | Callable[[QueryBuilderInterface], QueryBuilderInterface | None],
        as_: str,
        /,
    ) -> Self:
        subquery, bindings = self._create_subquery(query)
        return self.select_raw(f"({subquery}) AS {self._grammar.wrap(as_)}", *bindings)

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

    def distinct(self, *columns: str | ExpressionInterface) -> Self:
        self._distinct = list(columns) if columns else ["*"]
        return self

    def set_aggregate(self, function: str, *columns: str | ExpressionInterface) -> Self:
        self._aggregate = AggregateClause(function, list(columns))

        if not self._groups:
            self._orders = []
            self._bindings["order_by"] = []

        return self

    def from_(self, table: str, as_: str | None = None) -> Self:
        self._from = f"{table} as {as_}" if as_ else table
        return self

    @overload
    def with_query(self, name: str, query: QueryBuilderInterface, /) -> Self:
        """Add a CTE (Common Table Expression) to the query."""

    @overload
    def with_query(
        self,
        name: str,
        callback: Callable[[QueryBuilderInterface], QueryBuilderInterface | None],
        /,
    ) -> Self:
        """Add a CTE (Common Table Expression) to the query."""

    def with_query(
        self,
        name: str,
        query: QueryBuilderInterface
        | Callable[[QueryBuilderInterface], QueryBuilderInterface | None],
        /,
    ) -> Self:
        cte_query, bindings = self._create_subquery(query)
        self._ctes.append(f'"{name}" AS ({cte_query})')

        if bindings:
            self.add_binding(*bindings, type="with")

        return self

    @overload
    def join(
        self,
        expression: ExpressionInterface,
        callback: Callable[[JoinBuilderInterface], QueryBuilderInterface | None],
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
        callback: Callable[[JoinBuilderInterface], QueryBuilderInterface | None],
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
        left_operand: str
        | Callable[[JoinBuilderInterface], "QueryBuilderInterface | None"]
        | None = None,
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
    def join_lateral(self, query: QueryBuilderInterface, /, as_: str) -> Self:
        """Add a LATERAL JOIN clause to the query."""

    @overload
    def join_lateral(
        self,
        query: Callable[[QueryBuilderInterface], QueryBuilderInterface | None],
        /,
        as_: str,
    ) -> Self:
        """Add a LATERAL JOIN clause to the query."""

    def join_lateral(
        self,
        query: QueryBuilderInterface
        | Callable[[QueryBuilderInterface], QueryBuilderInterface | None],
        /,
        as_: str,
        type: str | None = None,
    ) -> Self:
        from pyrannic.database.query.join_lateral_builder import JoinLateralBuilder

        join_query, bindings = self._create_subquery(query)

        self._joins.append(
            JoinLateralBuilder(
                self,
                type or "inner",
                self.raw(f"({join_query}) as {self._grammar.wrap_table(as_)}"),
            )
        )
        self.add_binding(*bindings, type="join")

        return self

    @overload
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

    def join_sub(
        self,
        query: QueryBuilderInterface,
        as_: str,
        first_column: str
        | ExpressionInterface
        | Callable[[JoinBuilderInterface], QueryBuilderInterface | None],
        operator: str | None = None,
        second_column: str | ExpressionInterface | None = None,
        /,
        *,
        type: str | None = None,
        where: bool = False,
    ) -> Self:
        join_query, bindings = self._create_subquery(query)

        self.add_binding(*bindings, type="join")
        expression = f"({join_query}) as {self._grammar.wrap_table(as_)}"

        return self.join(
            Expression(expression),
            first_column,
            operator,
            second_column,
            type=type,
            where=where,
        )

    @overload
    def left_join_lateral(self, query: QueryBuilderInterface, /, as_: str) -> Self:
        """Add a LEFT LATERAL JOIN clause to the query."""

    @overload
    def left_join_lateral(
        self,
        query: Callable[[QueryBuilderInterface], QueryBuilderInterface | None],
        /,
        as_: str,
    ) -> Self:
        """Add a LEFT LATERAL JOIN clause to the query."""

    def left_join_lateral(
        self,
        query: QueryBuilderInterface
        | Callable[[QueryBuilderInterface], QueryBuilderInterface | None],
        /,
        as_: str,
    ) -> Self:
        return self.join_lateral(query, as_, type="left")  # type: ignore

    @overload
    def left_join(
        self,
        expression: "ExpressionInterface",
        callback: Callable[["JoinBuilderInterface"], "QueryBuilderInterface | None"],
        /,
    ) -> Self:
        """Add a LEFT JOIN clause to the query using a callback for the join condition."""

    @overload
    def left_join(
        self,
        table: str,
        callback: Callable[["JoinBuilderInterface"], "QueryBuilderInterface | None"],
        /,
    ) -> Self:
        """Add a LEFT JOIN clause to the query using a callback for the join condition."""

    @overload
    def left_join(
        self,
        table: str,
        left_operand: str,
        right_operand: str,
        /,
    ) -> Self:
        """Add a LEFT JOIN clause to the query."""

    @overload
    def left_join(
        self,
        table: str,
        left_operand: str,
        operator: str | None = None,
        right_operand: str | None = None,
        /,
    ) -> Self:
        """Add a LEFT JOIN clause to the query."""

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
        if callable(left_operand):
            return self.join(table_or_expression, left_operand, type="left")

        assert isinstance(table_or_expression, str), (
            "Table name must be provided for a LEFT JOIN"
        )
        assert left_operand is not None, "Left operand must be provided for a LEFT JOIN"

        return self.join(
            table_or_expression,
            left_operand,
            operator,
            right_operand,
            type="left",
        )

    @overload
    def left_join_sub(
        self,
        query: "QueryBuilderInterface",
        as_: str,
        callback: Callable[["JoinBuilderInterface"], "QueryBuilderInterface | None"],
        /,
    ) -> Self:
        """Add a LEFT JOIN subquery to the query."""

    @overload
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

    def left_join_sub(
        self,
        query: "QueryBuilderInterface",
        as_: str,
        first_column: 'str | ExpressionInterface | Callable[["JoinBuilderInterface"], "QueryBuilderInterface | None"]',
        operator: str | None = None,
        second_column: "str | ExpressionInterface | None" = None,
        /,
    ) -> Self:
        return self.join_sub(
            query,
            as_,
            first_column,  # pyright: ignore[reportArgumentType]
            operator,
            second_column,
            type="left",
        )

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

    def where_null(
        self,
        *columns: "str | ExpressionInterface",
        boolean: str = "and",
        not_: bool = False,
    ) -> Self:
        self._wheres.extend(
            WhereClause(col, boolean=boolean, type="not_null" if not_ else "null")
            for col in columns
        )

        return self

    def where_not_null(
        self,
        *column: str | ExpressionInterface,
        boolean: str = "and",
    ) -> Self:
        return self.where_null(*column, boolean=boolean, not_=True)

    def where_in(
        self,
        column: str | ExpressionInterface,
        values: list[Any],
        /,
        *,
        boolean: str = "and",
        not_: bool = False,
    ) -> Self:
        where_type = "not_in" if not_ else "in"
        self._wheres.append(WhereClause(column, "in", values, boolean, where_type))
        self.add_binding(*values, type="where")

        return self

    def or_where_in(
        self,
        column: str | ExpressionInterface,
        values: list[Any],
        /,
    ) -> Self:
        return self.where_in(column, values, boolean="or")

    def where_not_in(
        self,
        column: "str | ExpressionInterface",
        values: list[Any],
        /,
        *,
        boolean: str = "and",
    ) -> Self:
        return self.where_in(column, values, boolean=boolean, not_=True)

    def or_where_not_in(
        self,
        column: "str | ExpressionInterface",
        values: list[Any],
        /,
    ) -> Self:
        return self.where_not_in(column, values, boolean="or")

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

    def clean_bindings(self, bindings: list[Any]) -> list[Any]:
        return [b for b in bindings if not self._grammar.is_expression(b)]

    def _is_valid_operator(self, operator: str | None, /) -> bool:
        return isinstance(operator, str) and (
            operator in self.grammar.operators or operator in self._operators
        )

    def clone(self) -> Self:
        cloned = type(self)(self._grammar)
        cloned._columns = self._columns.copy()
        cloned._distinct = self._distinct
        cloned._from = self._from
        cloned._joins = self._joins.copy()
        cloned._wheres = self._wheres.copy()
        cloned._groups = self._groups.copy()
        cloned._orders = self._orders.copy()
        cloned._limit = self._limit
        cloned._offset = self._offset
        cloned._bindings = {k: v.copy() for k, v in self._bindings.items()}
        cloned._operators = self._operators.copy()

        return cloned

    @overload
    def clone_without(self, *attributes: str) -> Self:
        """Clone the query builder without the specified attributes."""

    @overload
    def clone_without(
        self,
        *,
        attributes: list[str],
        bindings: list[str],
    ) -> Self:
        """Clone the query builder without the specified attributes and bindings."""

    def clone_without(
        self,
        *args: str,
        attributes: list[str] | None = None,
        bindings: list[str] | None = None,
    ) -> Self:
        cloned = self.clone()
        attributes = list(args) if not attributes else attributes

        for attr in attributes:
            if attr == "from":
                cloned._from = ""
            elif isinstance(getattr(cloned, f"_{attr}", None), list):
                setattr(cloned, f"_{attr}", [])
            elif hasattr(cloned, f"_{attr}"):
                setattr(cloned, f"_{attr}", None)

        for binding in bindings or []:
            if binding in cloned._bindings:
                cloned._bindings[binding] = []

        return cloned

    def __copy__(self) -> Self:
        return self.clone()

    def __deepcopy__(self, memo: dict[int, Any]) -> Self:
        return self.clone()

    def _create_subquery(
        self,
        query: QueryBuilderInterface
        | Callable[[QueryBuilderInterface], QueryBuilderInterface | None],
    ) -> tuple[str, list[Any]]:
        if callable(query):
            subquery = type(self)(self._grammar)
            query(subquery)
        else:
            subquery = query

        return self._parse_subquery(subquery)

    def _parse_subquery(
        self,
        query: QueryBuilderInterface,
    ) -> tuple[str, list[Any]]:
        return query.to_sql(), query.get_bindings()
