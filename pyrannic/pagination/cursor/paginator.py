from typing import Any

from pyrannic.contracts.pagination.paginator import PaginatorInterface
from pyrannic.pagination.cursor.meta import PaginationMeta


class Paginator[ItemType](PaginatorInterface[ItemType, PaginationMeta]):
    """
    A generic class that describes a paginator based in cursor pagination.
    This exposes two public properties:

    - items: Allow us to get a list with all the items available in this paginator.
    - meta: Give us a PaginationMeta instance with meta information about the paginator.
    """

    __items: list[ItemType]
    __total: int = 0
    __per_page: int
    __previous_page: str | None
    __next_page: str | None
    __kwargs: dict[str, Any] | None

    def __init__(
        self,
        items: list[ItemType],
        per_page: int = 15,
        total: int = 0,
        previous_page: str | None = None,
        next_page: str | None = None,
        **kwargs: Any,
    ):
        self.__items = items
        self.__previous_page = previous_page
        self.__next_page = next_page
        self.__per_page = per_page
        self.__total = total
        self.__kwargs = kwargs

    @property
    def items(self) -> list[ItemType]:
        return self.__items

    def meta(self, meta_class: type[PaginationMeta] = PaginationMeta) -> PaginationMeta:
        return meta_class(
            previous_page=self.__previous_page,
            next_page=self.__next_page,
            per_page=self.__per_page,
            total=self.__total,
            **(self.__kwargs or {}),
        )

    def __repr__(self):
        return f"Paginator(meta={self.meta(PaginationMeta)!r})"
