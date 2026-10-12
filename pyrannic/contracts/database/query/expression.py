from abc import ABC, abstractmethod

from pyrannic.contracts.database.query.grammar import GrammarInterface


class ExpressionInterface(ABC):
    @abstractmethod
    def get_value(self, grammar: GrammarInterface | None = None) -> str | int | float:
        pass
