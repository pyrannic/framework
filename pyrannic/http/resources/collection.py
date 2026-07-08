from typing import Any, Generic, Sequence, TypeAlias, TypeVar, Union

from pydantic import BaseModel

from pyrannic.contracts.http.resources.collection import (
    ResourceCollectionInterface,
)
from pyrannic.contracts.http.resources.resource import ResourceInterface
from pyrannic.contracts.pagination.paginator import PaginatorInterface
from pyrannic.contracts.support.serializable import SerializableInterface
from pyrannic.pagination.meta import PaginationMeta
from pyrannic.support.reflection import get_generic_type

ResourceType = TypeVar("ResourceType", covariant=True, bound=ResourceInterface)

ItemsType: TypeAlias = Union[
    Sequence[ResourceType],
    Sequence[SerializableInterface],
    PaginatorInterface[SerializableInterface, PaginationMeta],
]


class _ResourceCollection(Generic[ResourceType], ResourceCollectionInterface):
    __resource_cls__: type[ResourceType]
    __meta_cls__: type[PaginationMeta] = PaginationMeta

    data: list[ResourceType]


class BaseCollection(BaseModel, _ResourceCollection[ResourceType]):
    def __init__(
        self,
        data: ItemsType[ResourceType],
        with_relationships: bool | list[str] = True,
        **kwargs: Any,
    ):
        if not hasattr(self, "__resource_cls__"):
            self.__resource_cls__ = get_generic_type(self)

        assert self.__resource_cls__ is not None, (
            "Resource class must be set before initializing ResourceCollection"
        )

        if isinstance(data, PaginatorInterface):
            super().__init__(
                data=[
                    self.__resource_cls__.from_model(model, with_relationships)
                    for model in data.items
                ],
                meta=data.meta(self.__meta_cls__),
            )
        elif len(data) == 0 or isinstance(data[0], dict):
            super().__init__(data=data or [], **kwargs)
        else:
            super().__init__(
                data=[
                    self.__resource_cls__.from_model(model, with_relationships)
                    for model in data
                ],
                **kwargs,
            )


class ResourceCollection(BaseCollection[ResourceType]):
    def __init__(self, items: ItemsType[ResourceType], /, **kwargs: Any) -> None:
        kwargs["data"] = items
        super().__init__(**kwargs)
