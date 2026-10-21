import re
from typing import Any, ClassVar

from pyrannic.contracts.database import (
    ExpressionInterface,
    GrammarInterface,
    JoinBuilderInterface,
    JoinLateralBuilderInterface,
    OrderByClauseInterface,
    QueryBuilderInterface,
    WhereClauseInterface,
)
from pyrannic.database.query.clauses.aggregate import AggregateClause
from pyrannic.support.collections import li
from pyrannic.support.collections.dict import flatten
from pyrannic.support.values import resolve_value

_IDENTIFIER_PATTERN: re.Pattern[str] = re.compile(
    r"^[a-zA-Z_][a-zA-Z0-9_]*(\.[a-zA-Z_][a-zA-Z0-9_]*)?$"
)


class Grammar(GrammarInterface):
    _select_components: ClassVar[dict[str, str]] = {
        "aggregate": "aggregate",
        "columns": "columns",
        "from_clause": "from_",
        "index_hint": "index_hint",
        "joins": "joins",
        "wheres": "wheres",
        "groups": "groups",
        "havings": "havings",
        "orders": "orders",
        "limit_count": "limit",
        "offset_count": "offset",
        "lock": "lock",
    }
    """Dict of components that make up a SELECT query in the correct order."""

    @property
    def operators(self) -> list[str]:
        return []

    def compile_select(self, query_builder: QueryBuilderInterface) -> str:
        # The user is not specifying any columns, so we default to selecting all columns.
        if not query_builder.columns and query_builder.from_clause:
            query_builder.select()

        sql = self._concatenate(*self._compile_components(query_builder)).strip()
        return sql

    def compile_exists(self, query_builder: QueryBuilderInterface) -> str:
        select = self.compile_select(query_builder)
        return f"SELECT exists({select}) AS {self.wrap('exists')}"

    def compile_insert(
        self,
        query_builder: QueryBuilderInterface,
        values: list[dict[str, Any]],
    ) -> str:
        table = self.wrap_table(query_builder.from_clause)
        columns = self.columnize(*values[0].keys())
        parameters = ", ".join(
            f"({self.parameterize(list(record.values()))})" for record in values
        )

        sql = f"INSERT INTO {table} ({columns}) VALUES {parameters}"

        return sql.strip()

    def compile_update(
        self,
        query_builder: QueryBuilderInterface,
        values: dict[str, Any],
    ) -> str:
        table = self.wrap_table(query_builder.from_clause)
        columns = self._compile_update_columns(values)
        where = self._compile_wheres(query_builder)
        joins = self._compile_joins(query_builder)

        if joins:
            sql = f"UPDATE {table} {joins} SET {columns} {where}"
        else:
            sql = f"UPDATE {table} SET {columns} {where}"

        return f"{sql}".strip()

    def _compile_update_columns(self, values: dict[str, Any]) -> str:
        return ", ".join(
            f"{self.wrap(k)} = {self.parameter(v)}" for k, v in values.items()
        )

    def _compile_components(
        self, query_builder: QueryBuilderInterface
    ) -> list[str | None]:
        """Compile the components necessary for a select clause."""

        sql: list[str | None] = []

        # We walk the components defined in `_select_components` to compile the SQL
        # segments querying the builder for those components.
        for key, method in self._select_components.items():
            value = getattr(query_builder, key, "")
            method = getattr(self, f"_compile_{method.strip('_')}", None)

            if value and method:
                sql.append(method(query_builder, value))

        return sql

    def _compile_aggregate(
        self,
        query_builder: QueryBuilderInterface,
        aggregate: AggregateClause,
    ) -> str | None:
        """Compile the SELECT portion of the query when an aggregate is present."""

        aggregate = aggregate or query_builder.aggregate

        if not aggregate:
            return None  # pragma: no cover

        function = aggregate.function.upper()
        columns = self.columnize(*aggregate.columns)

        return f"SELECT {function}({columns}) as {self.wrap('aggregate')}"

    def _compile_columns(
        self,
        query_builder: QueryBuilderInterface,
        columns: list[str | ExpressionInterface],
    ) -> str | None:
        """Compile the SELECT portion of the query."""

        # Let to the aggregate compiler to handle the SELECT clause when an aggregate is present.
        if query_builder.aggregate:
            return None

        select = "SELECT"

        if query_builder.is_distinct:
            select = f"{select} DISTINCT"

        return f"{select} {self.columnize(*columns)}"

    def _compile_from(
        self,
        _: QueryBuilderInterface,
        from_clause: str,
    ) -> str | None:
        """Compile the FROM portion of the query."""
        return f"FROM {self.wrap_table(from_clause)}"

    def _compile_joins(
        self,
        query_builder: QueryBuilderInterface,
        joins: list[JoinBuilderInterface] | None = None,
    ) -> str | None:
        """Compile the JOIN portion of the query."""

        joins = joins or query_builder.joins

        if not joins:
            return None  # pragma: no cover

        clauses: list[str] = []

        for join in joins:
            table = self.wrap_table(join.table)

            nested_joins = (
                ""
                if not join.joins
                else f" {self._compile_joins(query_builder, join.joins)}"
            )

            table_and_nested_joins = (
                table if not join.joins else f"({table}{nested_joins})"
            )

            if isinstance(join, JoinLateralBuilderInterface):
                clauses.append(self.compile_join_lateral(join, table_and_nested_joins))
            else:
                clauses.append(
                    f"{join.type.upper()} JOIN {table_and_nested_joins} {self._compile_wheres(join)}"
                )

        return " ".join(clauses)

    def _compile_wheres(
        self,
        query_builder: QueryBuilderInterface,
        wheres: list[WhereClauseInterface] | None = None,
    ) -> str | None:
        """Compile the WHERE portion of the query."""

        wheres = wheres or query_builder.wheres

        if not wheres:
            return None  # pragma: no cover

        sql: list[str] = []

        # We walk the all the where clauses and call the appropriate compile method for each.
        for where in wheres:
            method = getattr(self, f"_compile_where_{where.type}", None)

            if method:
                value = method(query_builder, where)
                if value:
                    sql.append(f"{where.boolean.upper()} {value}")

        conjunction = (
            "ON" if isinstance(query_builder, JoinBuilderInterface) else "WHERE"
        )

        return f"{conjunction} {self._remove_leading_boolean(' '.join(sql))}"

    def _compile_where_basic(
        self,
        _: QueryBuilderInterface,
        where: WhereClauseInterface,
    ) -> str | None:
        """Compile a basic WHERE clause."""
        assert not isinstance(where.value, list), (
            "Basic WHERE clause does not support list values. Use the WHERE IN clause instead."
        )

        value = self.parameter(where.value)
        return f"{self.wrap(where.column)} {where.operator} {value}"

    def _compile_where_in(
        self,
        _: QueryBuilderInterface,
        where: WhereClauseInterface,
    ) -> str | None:
        """Compile an IN WHERE clause."""
        assert isinstance(where.value, list) and where.value, (
            "IN WHERE clause requires a non-empty list of values"
        )

        return f"{self.wrap(where.column)} IN ({self.parameterize(where.value)})"

    def _compile_where_not_in(
        self,
        _: QueryBuilderInterface,
        where: WhereClauseInterface,
    ) -> str | None:
        """Compile a NOT IN WHERE clause."""
        assert isinstance(where.value, list) and where.value, (
            "NOT IN WHERE clause requires a non-empty list of values"
        )

        return f"{self.wrap(where.column)} NOT IN ({self.parameterize(where.value)})"

    def _compile_where_null(
        self,
        _: QueryBuilderInterface,
        where: WhereClauseInterface,
    ) -> str | None:
        """Compile a NULL WHERE clause."""
        return f"{self.wrap(where.column)} IS NULL"

    def _compile_where_not_null(
        self,
        _: QueryBuilderInterface,
        where: WhereClauseInterface,
    ) -> str | None:
        """Compile a NOT NULL WHERE clause."""
        return f"{self.wrap(where.column)} IS NOT NULL"

    def _compile_where_column(
        self,
        _: QueryBuilderInterface,
        where: WhereClauseInterface,
    ) -> str | None:
        """Compile a column-based WHERE clause."""
        assert where.value is not None and not isinstance(where.value, list), (
            "Column-based WHERE clause requires a value that is not a list or None"
        )
        return f"{self.wrap(where.column)} {where.operator} {self.wrap(where.value)}"

    def _compile_where_nested(
        self,
        query_builder: QueryBuilderInterface,
        where: WhereClauseInterface,
    ) -> str | None:
        """Compile a nested WHERE clause."""
        offset = 3 if isinstance(query_builder, JoinBuilderInterface) else 6
        sql = self._compile_wheres(where.query) or ""

        return f"({sql[offset:]})"

    def _compile_groups(
        self,
        query_builder: QueryBuilderInterface,
        groups: list[str | ExpressionInterface] | None = None,
    ) -> str | None:
        """Compile the GROUP BY portion of the query."""

        groups = groups or query_builder.groups

        if not groups:
            return None  # pragma: no cover

        return f"GROUP BY {self.columnize(*groups)}"

    def _compile_orders(
        self,
        query_builder: QueryBuilderInterface,
        orders: list[OrderByClauseInterface] | None = None,
    ) -> str | None:
        """Compile the ORDER BY portion of the query."""

        orders = orders or query_builder.orders

        if not orders:
            return None  # pragma: no cover

        sql: list[str] = []

        for order in orders:
            if order.expression is not None:
                sql.append(str(self.get_value(order.expression)))
            elif order.column is not None:
                sql.append(f"{self.wrap(order.column)} {order.direction.value.upper()}")

        return f"ORDER BY {', '.join(sql)}"

    def _compile_limit(self, _: QueryBuilderInterface, limit: Any) -> str | None:
        """Compile the LIMIT portion of the query."""
        return f"LIMIT {int(limit)}"

    def _compile_offset(self, _: QueryBuilderInterface, offset: Any) -> str | None:
        """Compile the OFFSET portion of the query."""
        return f"OFFSET {int(offset)}"

    def parameterize(
        self, values: list[str | float | bool | ExpressionInterface | None]
    ) -> str:
        return ", ".join([self.parameter(value) for value in values])

    def parameter(self, value: str | float | bool | ExpressionInterface | None) -> str:
        return (
            "%s"
            if value is None or not self.is_expression(value)
            else str(self.get_value(value))
        )

    def is_expression(self, value: Any) -> bool:
        return isinstance(value, ExpressionInterface)

    def get_value(
        self,
        expression: str | float | ExpressionInterface,
    ) -> str | int | float:
        if isinstance(expression, ExpressionInterface):
            return self.get_value(expression.get_value(self))

        return expression

    def wrap(self, value: str | float | ExpressionInterface) -> str:
        if isinstance(value, ExpressionInterface):
            return str(self.get_value(value))

        if isinstance(value, str) and " as " in value.lower():
            return self._wrap_aliased_value(value)

        return self._wrap_segments(str(value).split("."))

    def wrap_table(
        self,
        value: str | ExpressionInterface,
        prefix: str | None = None,
    ) -> str:
        if isinstance(value, ExpressionInterface):
            return str(self.get_value(value))

        return self._wrap_value(f"{prefix or ''}{value}")

    def _wrap_aliased_value(self, value: str) -> str:
        table, alias = re.split(r"\s+as\s+", value, maxsplit=1, flags=re.IGNORECASE)
        return f"{self.wrap(table)} AS {self._wrap_value(alias)}"

    def _wrap_segments(self, values: list[str]) -> str:
        count = len(values)

        return ".".join([
            self.wrap_table(value)
            if count > 1 and index == 0
            else self._wrap_value(value)
            for index, value in enumerate(values)
        ])

    def _wrap_value(self, value: str) -> str:
        if value == "*":
            return value

        value = self._normalize_identifier_token(value)

        # Ensure that table and column names are secure.
        if not _IDENTIFIER_PATTERN.match(value):
            raise ValueError(f"Invalid or insecure SQL identifier: '{value}'")

        return f'"{value}"'

    def _normalize_identifier_token(self, value: str) -> str:
        if '"' not in value:
            return value

        # Accept pre-quoted segments like "users" and normalize to raw token.
        if value.startswith('"') and value.endswith('"'):
            token = value[1:-1]
            if '"' in token:
                raise ValueError(f"Invalid or insecure SQL identifier: '{value}'")

            return token

        raise ValueError(f"Invalid or insecure SQL identifier: '{value}'")

    def columnize(self, *columns: str | ExpressionInterface) -> str:
        return ", ".join([self.wrap(column) for column in columns])

    def quote_string(self, value: str) -> str:
        # TODO - Implement proper escaping using the right connection and database driver.
        return f"'{value}'"

    def escape(self, value: str | float | bool | None, binary: bool = False) -> str:
        if value is None:
            return "null"
        elif binary:
            assert isinstance(value, str)
            return self._escape_binary(value)
        elif isinstance(value, bool):
            return self._escape_boolean(value)
        elif isinstance(value, float | int):
            return str(value)

        return self._escape_string(value)

    def _escape_string(self, value: str) -> str:
        return self.quote_string(value)

    def _escape_binary(self, value: str) -> str:
        raise NotImplementedError()

    def _escape_boolean(self, value: bool) -> str:
        return "1" if value else "0"

    def _concatenate(self, *segments: str | None, separator: str = " ") -> str:
        """Concatenate multiple SQL segments with the replacement separator, removing empty segments."""
        return separator.join(segment for segment in segments if segment)

    def _remove_leading_boolean(self, value: str) -> str:
        """Remove the leading boolean operator (AND/OR) from a statement if present."""
        return re.sub(r"^(AND|OR)\s+", "", value, flags=re.IGNORECASE)

    def substitute_bindings_into_raw_sql(self, sql: str, bindings: list[Any]) -> str:
        for binding in bindings:
            sql = sql.replace("%s", self.escape(binding), 1)

        return sql

    def prepare_bindings_for_update(
        self,
        bindings: dict[str, list[Any]],
        values: dict[str, Any],
    ) -> list[Any]:
        clean_bindings = {k: v for k, v in bindings.items() if k != "select"}
        val = li.flatten([resolve_value(v) for v in values.values()])

        return val + flatten(clean_bindings)
