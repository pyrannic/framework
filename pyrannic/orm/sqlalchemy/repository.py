from typing import Any, Tuple, cast

from pyrannic.contracts.orm.repository import RepositoryInterface, T
from pyrannic.contracts.pagination.paginator import PaginatorInterface
from pyrannic.orm.sqlalchemy.query_builder import QueryBuilder
from pyrannic.pagination.paginator import Paginator

from sqlalchemy.sql.selectable import TypedReturnsRows


class Repository(QueryBuilder[T], RepositoryInterface[T]):
    def create(self, model: T) -> T:
        try:
            self.session.add(model)
            self.session.commit()
            self.session.refresh(model)
            return model
        except Exception as e:
            self.session.rollback()
            self._logger.exception(f"Rolling Back. Error inserting model: {e}")
            raise

    def update(self, model: T) -> T:
        try:
            self.session.merge(model)
            self.session.commit()
            return model
        except Exception as e:
            self.session.rollback()
            self._logger.exception(f"Rolling Back. Error updating model: {e}")
            raise

    def destroy(self, model: T | None = None) -> None:
        self._prepare_destroy_model_if_needed(model)
        self._before_query()

        try:
            self.session.execute(cast(TypedReturnsRows[Tuple[T]], self._query))
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            self._logger.exception(f"Rolling Back. Error destroying model: {e}")
            raise
        finally:
            self._reset_query()

    def remove(self, model: T) -> T:
        return self.update(model) if self._remove_model(model) else model

    def restore(self, model: T) -> T:
        return self.update(model) if self._restore_model(model) else model

    def count(self) -> int:
        self._before_query()
        return self._count(reset_query=False)

    def first(self) -> T | None:
        self._before_query()
        model = (
            self.session.scalars(cast(TypedReturnsRows[Tuple[T]], self._query))
        ).first()
        self._reset_query()

        return model

    def all(self) -> list[T]:
        return self.get()

    def get(self) -> list[T]:
        self._before_query()
        return self._get()

    def find(self, value: Any) -> T | None:
        return self.select().where(self.__model__.primary_key_column() == value).first()

    def paginate(
        self,
        page: int = 1,
        per_page: int | None = None,
        **kwargs: Any,
    ) -> PaginatorInterface[T, Any]:
        self._prepare_query()
        self._before_query()

        total = self._count(reset_query=False)
        page, per_page, last_page = self._apply_pagination(total, page, per_page)
        items = self._get()

        return Paginator(items, page, per_page, total, last_page, **kwargs)

    def _get(self) -> list[T]:
        models = (
            self.session.scalars(cast(TypedReturnsRows[Tuple[T]], self._query))
        ).all()
        self._reset_query()

        return list(models)

    def _count(self, reset_query: bool = True) -> int:
        count = self.session.execute(
            cast(TypedReturnsRows[Tuple[int]], self._get_count_query)
        ).scalar()

        if reset_query:
            self._reset_query()

        return count or 0
