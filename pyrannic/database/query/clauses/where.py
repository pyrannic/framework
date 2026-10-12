from typing import Any, Self

from pyrannic.contracts.database.query.clauses.where import WhereClauseInterface
from pyrannic.contracts.database.query.expression import ExpressionInterface
from pyrannic.database.query.builder import QueryBuilderInterface


class WhereClause(WhereClauseInterface):
    _type: str
    _query: QueryBuilderInterface | None = None
    _column: str | ExpressionInterface | None = None
    _value: Any | ExpressionInterface | None = None
    _operator: str = "="
    _boolean: str = "and"

    def __init__(
        self,
        column: str | ExpressionInterface | None = None,
        operator: str = "=",
        value: Any | None = None,
        boolean: str = "and",
        type: str = "basic",
        query: QueryBuilderInterface | None = None,
    ) -> None:
        super().__init__()
        self._type = type
        self._column = column
        self._value = value
        self._operator = operator
        self._boolean = boolean
        self._query = query

    @classmethod
    def nested(cls, query: QueryBuilderInterface, boolean: str = "and") -> Self:
        return cls(
            query=query,
            boolean=boolean,
            type="nested",
        )

    @property
    def type(self) -> str:
        return self._type

    @property
    def query(self) -> QueryBuilderInterface:
        assert self._query is not None, (
            "Query should not be None for a nested where clause."
        )
        return self._query

    @property
    def column(self) -> str | ExpressionInterface:
        assert self._column is not None, (
            "Column should not be None for a basic where clause."
        )
        return self._column

    @property
    def value(self) -> Any | ExpressionInterface | None:
        return self._value

    @property
    def operator(self) -> str:
        return self._operator

    @property
    def boolean(self) -> str:
        return self._boolean

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, WhereClause):
            return False
        return (
            self._type == other._type
            and self._column == other._column
            and self._value == other._value
            and self._operator == other._operator
            and self._boolean == other._boolean
        )

    def __repr__(self) -> str:
        return (
            f"WhereClause(column={self._column!r}, operator={self._operator!r}, "
            f"value={self._value!r}, boolean={self._boolean!r}, type={self._type!r})"
        )
