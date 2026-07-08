from abc import ABC, abstractmethod
from typing import Generic, TypeVar

ItemType = TypeVar("ItemType", covariant=True)
MetaType = TypeVar("MetaType")


class PaginatorInterface(ABC, Generic[ItemType, MetaType]):
    """
    A generic class that describes a paginator. This exposes two public properties:

    - items: Allow us to get a list with all the items available in this paginator.
    - meta: Give us a PaginationMeta instance with meta information about the paginator.
    """

    @property
    @abstractmethod
    def items(self) -> list[ItemType]:
        pass

    @abstractmethod
    def meta(self, meta_class: type[MetaType]) -> MetaType:
        pass
