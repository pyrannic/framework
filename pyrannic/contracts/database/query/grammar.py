from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any

from pyrannic.contracts.database.query.builder import QueryBuilderInterface
from pyrannic.contracts.database.query.join_lateral_builder import (
    JoinLateralBuilderInterface,
)

if TYPE_CHECKING:
    from pyrannic.contracts.database.query.expression import ExpressionInterface


class GrammarInterface(ABC):
    @property
    @abstractmethod
    def operators(self) -> list[str]:
        """
        List of valid grammar specific SQL operators.
        """

    @abstractmethod
    def compile_select(self, query_builder: QueryBuilderInterface) -> str:
        """
        Compile a SELECT query into its SQL representation.
        """

    def compile_join_lateral(
        self,
        join: JoinLateralBuilderInterface,
        expression: str,
    ) -> str:
        """
        Compile a lateral join clause.
        """
        raise NotImplementedError(
            "This database engine does not support lateral joins."
        )

    @abstractmethod
    def get_value(
        self,
        expression: "str | float | ExpressionInterface",
    ) -> str | int | float:
        """
        Transforms expressions to their scalar types.
        """

    @abstractmethod
    def wrap(self, value: "str | ExpressionInterface") -> str:
        """
        Wrap a value in keyword identifiers.
        """

    @abstractmethod
    def wrap_table(
        self,
        value: "str | ExpressionInterface",
        prefix: str | None = None,
    ) -> str:
        """
        Wrap a table in keyword identifiers.
        """

    @abstractmethod
    def columnize(self, *columns: "str | ExpressionInterface") -> str:
        """
        Convert a list of column names into a delimited string.
        """

    @abstractmethod
    def quote_string(self, value: str) -> str:
        """
        Quote the given string literal.
        """

    @abstractmethod
    def escape(self, value: str | float | bool | None, binary: bool = False) -> str:
        """
        Escapes a value for safe SQL embedding.
        """

    @abstractmethod
    def substitute_bindings_into_raw_sql(self, sql: str, bindings: list[Any]) -> str:
        """
        Substitute the given bindings into the raw SQL string.
        """
