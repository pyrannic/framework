from pydantic import BaseModel, Field
from pyrannic.contracts.pagination.meta import PaginationMetaInterface


class PaginationMeta(BaseModel, PaginationMetaInterface):
    """
    Class to be used together with a cursor-based paginator as its meta information.
    In this way, a collection response can have meta information such as cursors for the previous and next pages,
    number of items per page, and total number of items.
    """

    previous_page: str | None = Field(
        default=None,
        description="Cursor for the previous page",
    )

    next_page: str | None = Field(default=None, description="Cursor for the next page")
    per_page: int = Field(default=15, ge=1, description="Number of items per page")
    total: int | None = Field(default=None, ge=0, description="Total number of items")

    def __repr__(self):
        return f"PaginationMeta(previous_page={self.previous_page!r}, next_page={self.next_page!r}, per_page={self.per_page!r}, total={self.total!r})"
