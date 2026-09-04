from abc import ABC, abstractmethod
from typing import Any

from pyrannic.contracts.pagination.paginator import PaginatorInterface


class AsyncRepositoryInterface[T](ABC):
    @abstractmethod
    async def create(self, model: T) -> T:
        """Insert a new record into the database."""

    @abstractmethod
    async def update(self, model: T) -> T:
        """Update an existing record in the database."""

    @abstractmethod
    async def destroy(self, model: T | None = None) -> None:
        """Permanently delete the records matching the current query."""

    @abstractmethod
    async def remove(self, model: T) -> T:
        """
        Soft delete the models by setting the deleted_at timestamp.
        The model must implement the SoftDeletesInterface mixin for this to work.
        """

    @abstractmethod
    async def restore(self, model: T) -> T:
        """
        Restore a soft-deleted model by clearing the deleted_at timestamp.
        The model must implement the SoftDeletesInterface mixin for this to work.
        """

    @abstractmethod
    async def count(self) -> int:
        """Count the number of records matching the current query."""

    @abstractmethod
    async def first(self) -> T | None:
        """Retrieve the first record of the model."""

    @abstractmethod
    async def all(self) -> list[T]:
        """Retrieve all records matching the current query. Alias for get()"""

    @abstractmethod
    async def get(self) -> list[T]:
        """Retrieve all records matching the current query. Alias for all()"""

    @abstractmethod
    async def find(self, value: Any) -> T | None:
        """Find a record by its primary key."""

    @abstractmethod
    async def paginate(
        self,
        page: int = 1,
        per_page: int | None = None,
        **kwargs: Any,
    ) -> PaginatorInterface[T, Any]:
        """Paginate the results of the current query."""
