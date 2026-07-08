from typing import Any, Tuple, cast

from pyrannic.contracts.orm.async_repository import RepositoryInterface, T
from pyrannic.contracts.pagination.paginator import PaginatorInterface
from pyrannic.orm.sqlalchemy.async_query_builder import AsyncQueryBuilder
from pyrannic.pagination.paginator import Paginator

from sqlalchemy.sql.selectable import TypedReturnsRows


class AsyncRepository(AsyncQueryBuilder[T], RepositoryInterface[T]):
    async def create(self, model: T) -> T:
        try:
            self.session.add(model)
            await self.session.commit()
            await self.session.refresh(model)
            return model
        except Exception as e:
            await self.session.rollback()
            self._logger.exception(f"Rolling Back. Error inserting object: {e}")
            raise

    async def update(self, model: T) -> T:
        try:
            await self.session.merge(model)
            await self.session.commit()
            return model
        except Exception as e:
            await self.session.rollback()
            self._logger.exception(f"Rolling Back. Error updating model: {e}")
            raise

    async def destroy(self, model: T | None = None) -> None:
        self._prepare_destroy_model_if_needed(model)
        self._before_query()

        try:
            await self.session.execute(cast(TypedReturnsRows[Tuple[T]], self._query))
            await self.session.commit()
        except Exception as e:
            await self.session.rollback()
            self._logger.exception(f"Rolling Back. Error destroying model: {e}")
            raise
        finally:
            self._reset_query()

    async def remove(self, model: T) -> T:
        return (await self.update(model)) if self._remove_model(model) else model

    async def restore(self, model: T) -> T:
        return (await self.update(model)) if self._restore_model(model) else model

    async def count(self) -> int:
        self._before_query()
        return await self._count(reset_query=False)

    async def first(self) -> T | None:
        self._before_query()
        model = (
            await self.session.scalars(cast(TypedReturnsRows[Tuple[T]], self._query))
        ).first()
        self._reset_query()

        return model

    async def all(self) -> list[T]:
        return await self.get()

    async def get(self) -> list[T]:
        self._before_query()
        return await self._get()

    async def find(self, value: Any) -> T | None:
        return await (
            self.select().where(self.__model__.primary_key_column() == value).first()
        )

    async def paginate(
        self,
        page: int = 1,
        per_page: int | None = None,
        **kwargs: Any,
    ) -> PaginatorInterface[T, Any]:
        self._prepare_query()
        self._before_query()

        total = await self._count(reset_query=False)
        page, per_page, last_page = self._apply_pagination(total, page, per_page)
        items = await self._get()

        return Paginator(items, page, per_page, total, last_page, **kwargs)

    async def _get(self) -> list[T]:
        models = (
            await self.session.scalars(cast(TypedReturnsRows[Tuple[T]], self._query))
        ).all()
        self._reset_query()

        return list(models)

    async def _count(self, reset_query: bool = True) -> int:
        count = (
            await self.session.execute(
                cast(TypedReturnsRows[Tuple[int]], self._get_count_query)
            )
        ).scalar()

        if reset_query:
            self._reset_query()

        return count or 0
