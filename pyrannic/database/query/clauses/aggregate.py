from pyrannic.contracts.database import (
    AggregateClauseInterface,
    ExpressionInterface,
)


class AggregateClause(AggregateClauseInterface):
    _function: str
    _columns: list[str | ExpressionInterface]

    def __init__(
        self,
        function: str,
        columns: list[str | ExpressionInterface],
    ) -> None:
        super().__init__()
        self._function = function
        self._columns = columns

    @property
    def function(self) -> str:
        return self._function

    @property
    def columns(self) -> list[str | ExpressionInterface]:
        return self._columns

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, AggregateClause):
            return False

        return self._function == other._function and self._columns == other._columns

    def __repr__(self) -> str:
        return (
            f"AggregateClause(function={self._function!r}, columns={self._columns!r})"
        )
