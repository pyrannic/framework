from pyrannic.contracts.database.query.expression import ExpressionInterface
from pyrannic.contracts.database.query.grammar import GrammarInterface


class Expression(ExpressionInterface):
    def __init__(self, value: str | float) -> None:
        self._value = value

    def get_value(self, grammar: GrammarInterface | None = None) -> str | int | float:
        return self._value

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Expression):
            return False

        return self._value == other._value
