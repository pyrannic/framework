from abc import abstractmethod
import math
from datetime import datetime
from logging import Logger
from typing import Any, Self, overload

from pyrannic.contracts.orm.mixins.soft_deletes import SoftDeletesInterface
from pyrannic.contracts.orm.query_builder import QueryBuilderInterface
from pyrannic.contracts.orm.repository import T
from pyrannic.contracts.orm.scope import ScopeInterface
from pyrannic.orm.sqlalchemy.scopes.soft_deleting_scope import SoftDeletingScope
from pyrannic.support.datetime import get_current_utc_datetime
from pyrannic.support.reflection import get_generic_type
from sqlalchemy import (
    ColumnExpressionArgument,
    CompoundSelect,
    Delete,
    Select,
    UnaryExpression,
    column,
    delete,
    func,
    select,
)
from sqlalchemy.orm import InstrumentedAttribute


class AbstractQueryBuilder(QueryBuilderInterface[T]):
    __model__: type[T]
    __scopes__: list[ScopeInterface[T]]

    _scopes: list[ScopeInterface[T]]
    _query: Select[Any] | Delete | CompoundSelect[Any] | None = None
    _is_ordering: bool = False
    _soft_deleting_scope: SoftDeletingScope[T]

    def __init__(self, logger: Logger):
        if not hasattr(self, "__model__"):
            self.__model__ = get_generic_type(self)

        if not hasattr(self, "__scopes__"):
            self.__scopes__ = []

        self._logger = logger

        self._soft_deleting_scope = SoftDeletingScope()
        self._scopes = []

        self._scopes.append(self._soft_deleting_scope)
        self._scopes.extend(self.__scopes__)

    @property
    @abstractmethod
    def session(self) -> Any:
        """Subclasses must implement the 'session' property."""

    @property
    def model(self) -> type[T]:
        return self.__model__

    def select(self, model: type[T] | None = None) -> Self:
        self._query = select(model or self.model)
        return self

    def delete(self, model: type[T] | None = None) -> Self:
        self._query = delete(model or self.model)
        return self

    def order_by(
        self,
        *attributes: str | InstrumentedAttribute[Any] | UnaryExpression[Any],
    ) -> Self:
        self._prepare_query()

        if isinstance(self._query, (Select, CompoundSelect)):
            self._is_ordering = True
            self._query = self._query.order_by(*attributes)

        return self

    def limit(self, limit: int | None) -> Self:
        self._prepare_query()

        if limit is not None and limit > 0 and isinstance(self._query, Select):
            self._query = self._query.limit(limit)

        return self

    def offset(self, offset: int | None) -> Self:
        self._prepare_query()

        if offset is not None and offset > 0 and isinstance(self._query, Select):
            self._query = self._query.offset(offset)

        return self

    @overload
    def where(self, *where_clause: ColumnExpressionArgument[Any]) -> Self: ...

    @overload
    def where(self, **kwargs: Any) -> Self: ...

    def where(
        self,
        *where_clause: ColumnExpressionArgument[Any],
        **kwargs: Any,
    ) -> Self:
        self._prepare_query()

        if isinstance(self._query, (Select, Delete)):
            if where_clause:
                self._query = self._query.where(*where_clause)
            elif kwargs:
                self._query = self._query.filter_by(**kwargs)

        return self

    def where_none(self, column_name: str) -> Self:
        return self.where(column(column_name).is_(None))

    def where_not_none(self, column_name: str) -> Self:
        return self.where(column(column_name).isnot(None))

    def filter(self, *filters: ColumnExpressionArgument[Any] | None) -> Self:
        self._prepare_query()

        if isinstance(self._query, (Select, Delete)):
            filters = tuple(v for v in filters if v is not None)
            self._query = self._query.where(*filters)

        return self

    def filter_by(self, **kwargs: Any) -> Self:
        self._prepare_query()

        if isinstance(self._query, (Select, Delete)):
            self._query = self._query.filter_by(**kwargs)

        return self

    def group_by(
        self,
        *attributes: str | InstrumentedAttribute[Any] | UnaryExpression[Any],
    ) -> Self:
        self._prepare_query()

        if isinstance(self._query, (Select, CompoundSelect)):
            self._query = self._query.group_by(*attributes)

        return self

    def with_removed(self) -> Self:
        if self._supports_soft_deletion():
            self._soft_deleting_scope.set_with_removed()

        return self

    def only_removed(self) -> Self:
        if self._supports_soft_deletion():
            self._soft_deleting_scope.set_only_removed()

        return self

    def _supports_soft_deletion(self) -> bool:
        return issubclass(self.model, SoftDeletesInterface)

    def _reset_query(self) -> None:
        self._soft_deleting_scope.reset()
        self._query = None
        self._is_ordering = False

    @property
    def _get_count_query(self) -> Select[Any]:
        assert isinstance(self._query, Select)

        return (
            self._query.with_only_columns(func.count(), maintain_column_froms=True)
            .order_by(None)
            .limit(None)
            .offset(None)
        )

    @staticmethod
    def _resolve_page(page: int | None = 1) -> int:
        if page is None or page <= 0:
            return 1

        return page

    @staticmethod
    def _resolve_last_page(last_page: int | None = None) -> int:
        if last_page is None or last_page <= 0:
            return 1

        return last_page

    def _prepare_query(self) -> None:
        if self._query is None:
            self.select()

    def _before_query(self) -> None:
        assert self._query is not None
        self._apply_scopes()

    def _apply_scopes(self) -> Self:
        for scope in self._scopes:
            scope.apply(self)

        return self

    def _apply_pagination(
        self,
        total: int = 0,
        page: int = 1,
        per_page: int | None = None,
    ) -> tuple[int, int, int]:
        if not self._is_ordering:
            self.order_by(self.model.primary_key_column().asc())

        if per_page is None or per_page <= 0:
            per_page = max(total, 1)
            last_page = 1
            page = 1
        else:
            last_page = self._resolve_last_page(math.ceil(total / per_page))
            page = self._resolve_page(page)

            count = per_page
            offset = (page - 1) * per_page

            self.limit(count).offset(offset)

        return page, per_page, last_page

    def _prepare_destroy_model_if_needed(self, model: T | None) -> None:
        if model is not None:
            self.delete().where(
                self.model.primary_key_column() == model.primary_key_value
            )

    def _prepare_soft_deletes_model(
        self,
        model: T,
        deleted_at: datetime | None,
    ) -> bool:
        if isinstance(model, SoftDeletesInterface):
            model.set_deleted_at(deleted_at)
            return True

        return False

    def _remove_model(self, model: T) -> bool:
        return self._prepare_soft_deletes_model(model, get_current_utc_datetime())

    def _restore_model(self, model: T) -> bool:
        return self._prepare_soft_deletes_model(model, None)
