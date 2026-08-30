from abc import ABC, abstractmethod
from typing import TypeVar

ItemType_co = TypeVar("ItemType_co", covariant=True)
MetaType = TypeVar("MetaType")


class PaginatorInterface[ItemType_co, MetaType](ABC):
    """
    A generic class that describes a paginator. This exposes two public properties:

    - items: Allow us to get a list with all the items available in this paginator.
    - meta: Give us a PaginationMeta instance with meta information about the paginator.
    """

    @property
    @abstractmethod
    def items(self) -> list[ItemType_co]:
        pass

    @abstractmethod
    def meta(self, meta_class: type[MetaType]) -> MetaType:
        pass
