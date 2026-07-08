import math
from typing import Any, TypeVar

from pyrannic.contracts.pagination.paginator import PaginatorInterface
from pyrannic.pagination.meta import PaginationMeta

ItemType = TypeVar("ItemType", covariant=True)


class Paginator(PaginatorInterface[ItemType, PaginationMeta]):
    """
    A generic class that describes a paginator. This exposes two public properties:

    - items: Allow us to get a list with all the items available in this paginator.
    - meta: Give us a PaginationMeta instance with meta information about the paginator.
    """

    __items: list[ItemType]
    __page: int = 1
    __total: int = 0
    __per_page: int
    __last_page: int | None
    __kwargs: dict[str, Any] | None

    def __init__(
        self,
        items: list[ItemType],
        page: int = 1,
        per_page: int = 15,
        total: int = 0,
        last_page: int = 1,
        **kwargs: Any,
    ):
        self.__items = items
        self.__page = page
        self.__per_page = per_page
        self.__total = total
        self.__last_page = last_page
        self.__kwargs = kwargs

    @property
    def items(self) -> list[ItemType]:
        return self.__items

    def meta(self, meta_class: type[PaginationMeta] = PaginationMeta) -> PaginationMeta:
        return meta_class(
            current_page=self.__page,
            last_page=self.__last_page or math.ceil(self.__total / self.__per_page),
            per_page=self.__per_page,
            total=self.__total,
            from_index=0
            if self.__total == 0
            else (self.__page - 1) * self.__per_page + 1,
            to_index=min(self.__page * self.__per_page, self.__total),
            **(self.__kwargs or {}),
        )

    def __repr__(self):
        return f"Paginator(meta={self.meta(PaginationMeta)!r})"
