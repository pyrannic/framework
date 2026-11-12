from typing import Self

from pyrannic.contracts.database import (
    SetClauseInterface,
)
from pyrannic.contracts.database.query.builder import QueryBuilderInterface


class SetClause(SetClauseInterface):
    _query: QueryBuilderInterface
    _type: str

    def __init__(self, query: QueryBuilderInterface, type: str) -> None:
        self._query = query
        self._type = type

    @classmethod
    def union(cls, query: QueryBuilderInterface) -> Self:
        return cls(query, "UNION")

    @classmethod
    def intersect(cls, query: QueryBuilderInterface) -> Self:
        return cls(query, "INTERSECT")

    @classmethod
    def except_(cls, query: QueryBuilderInterface) -> Self:
        return cls(query, "EXCEPT")

    @property
    def type(self) -> str:
        return self._type

    @property
    def query(self) -> QueryBuilderInterface:
        return self._query

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, SetClause):
            return False

        return self._query == other._query and self._type == other._type

    def __repr__(self) -> str:
        return f"SetClause(query={self._query!r}, type={self._type!r})"
