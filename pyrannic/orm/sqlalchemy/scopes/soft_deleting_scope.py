from pyrannic.contracts.orm.mixins.soft_deletes import SoftDeletesInterface
from pyrannic.contracts.orm.query_builder import QueryBuilderInterface, T
from pyrannic.contracts.orm.scope import ScopeInterface


class SoftDeletingScope(ScopeInterface[T]):
    """
    A scope that automatically excludes soft-deleted records from query results.
    This scope can be applied to repositories that manage models implementing the SoftDeletesInterface.
    """

    _only_removed: bool = False
    _with_removed: bool = False

    def apply(self, repository: QueryBuilderInterface[T]) -> None:
        if issubclass(repository.model, SoftDeletesInterface):
            if self._only_removed:
                repository.where_not_none(repository.model.deleted_at_column())
            elif not self._with_removed:
                repository.where_none(repository.model.deleted_at_column())

    def set_only_removed(self) -> None:
        self._only_removed = True
        self._with_removed = False

    def set_with_removed(self) -> None:
        self._with_removed = True
        self._only_removed = False

    def reset(self) -> None:
        self._only_removed = False
        self._with_removed = False
