from abc import ABC, abstractmethod
from collections.abc import Sequence

from pyrannic.contracts.pagination.meta import PaginationMetaInterface


class PaginatorInterface[ItemType](ABC):
    """
    A generic class that describes a paginator. This exposes two public properties:

    - items: Allow us to get a list with all the items available in this paginator.
    - meta: Give us a PaginationMeta instance with meta information about the paginator.
    """

    @property
    @abstractmethod
    def items(self) -> Sequence[ItemType]:
        pass

    @abstractmethod
    def meta(
        self,
        meta_class: type[PaginationMetaInterface],
    ) -> PaginationMetaInterface:
        pass
