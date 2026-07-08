from abc import ABC, abstractmethod
from typing import Any, Generic

from pyrannic.contracts.orm.query_builder import T
from pyrannic.contracts.pagination.paginator import PaginatorInterface


class RepositoryInterface(ABC, Generic[T]):
    @abstractmethod
    async def create(self, model: T) -> T:
        """Insert a new record into the database."""
        pass

    @abstractmethod
    async def update(self, model: T) -> T:
        """Update an existing record in the database."""
        pass

    @abstractmethod
    async def destroy(self, model: T | None = None) -> None:
        """Permanently delete the records matching the current query."""
        pass

    @abstractmethod
    async def remove(self, model: T) -> T:
        """
        Soft delete the models by setting the deleted_at timestamp.
        The model must implement the SoftDeletesInterface mixin for this to work.
        """
        pass

    @abstractmethod
    async def restore(self, model: T) -> T:
        """
        Restore a soft-deleted model by clearing the deleted_at timestamp.
        The model must implement the SoftDeletesInterface mixin for this to work.
        """
        pass

    @abstractmethod
    async def count(self) -> int:
        """Count the number of records matching the current query."""
        pass

    @abstractmethod
    async def first(self) -> T | None:
        """Retrieve the first record of the model."""
        pass

    @abstractmethod
    async def all(self) -> list[T]:
        """Retrieve all records matching the current query. Alias for get()"""
        pass

    @abstractmethod
    async def get(self) -> list[T]:
        """Retrieve all records matching the current query. Alias for all()"""
        pass

    @abstractmethod
    async def find(self, value: Any) -> T | None:
        """Find a record by its primary key."""
        pass

    @abstractmethod
    async def paginate(
        self,
        page: int = 1,
        per_page: int | None = None,
        **kwargs: Any,
    ) -> PaginatorInterface[T, Any]:
        """Paginate the results of the current query."""
        pass
