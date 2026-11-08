from pyrannic.contracts.database import HavingClauseInterface
from pyrannic.database.query.clauses.where import WhereClause


class HavingClause(WhereClause, HavingClauseInterface):
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, HavingClause):
            return False
        return super().__eq__(other)

    def __repr__(self) -> str:
        return (
            f"HavingClause(column={self._column!r}, operator={self._operator!r}, "
            f"value={self._value!r}, boolean={self._boolean!r}, type={self._type!r})"
        )
