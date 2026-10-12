from pyrannic.contracts.database import (
    ExpressionInterface,
    OrderByClauseInterface,
    SortDirection,
)


class OrderByClause(OrderByClauseInterface):
    _column: str | ExpressionInterface
    _direction: SortDirection = SortDirection.ASC

    def __init__(
        self,
        column: str | ExpressionInterface,
        direction: SortDirection = SortDirection.ASC,
    ) -> None:
        super().__init__()
        self._column = column
        self._direction = direction

    @property
    def is_raw(self) -> bool:
        return isinstance(self._column, ExpressionInterface)

    @property
    def expression(self) -> ExpressionInterface | None:
        if isinstance(self._column, ExpressionInterface):
            return self._column

        return None

    @property
    def column(self) -> str | None:
        if isinstance(self._column, str):
            return self._column

        return None

    @property
    def direction(self) -> SortDirection:
        return self._direction

    def _get_compiled(self) -> str:
        if isinstance(self._column, ExpressionInterface):
            return str(self._column.get_value()).lower()

        return f"{self._column} {self._direction.value}".lower()

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, OrderByClause):
            return False

        return self._get_compiled() == other._get_compiled()

    def __repr__(self) -> str:
        if self.is_raw:
            return f"OrderByClause(expression={self._column!r})"

        return f"OrderByClause(column={self._column!r}, direction={self._direction.value!r})"
