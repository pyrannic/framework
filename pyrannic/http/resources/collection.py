from typing import Any, Generic, Sequence, TypeAlias, TypeVar, Union

from pydantic import BaseModel, model_serializer

from pyrannic.contracts.http.resources.collection import (
    ResourceCollectionInterface,
)
from pyrannic.contracts.http.resources.resource import ResourceInterface
from pyrannic.contracts.pagination.paginator import PaginatorInterface
from pyrannic.contracts.support.serializable import SerializableInterface
from pyrannic.pagination.meta import PaginationMeta
from pyrannic.support.reflection import get_generic_type, is_optional

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
        else:
            if not is_optional(self.__class__, "meta"):
                raise RuntimeError(
                    "\n\n"
                    "   The 'meta' attribute is defined as required in your ResourceCollection subclass.\n"
                    "   To fix this exception you have three options:\n"
                    "    1. Instead of providing your items collection as a list, use a PaginatorInterface to provide the items.\n"
                    "    2. Make the 'meta' attribute optional in your ResourceCollection subclass. E.g.:\n"
                    "       class MyResourceCollection(ResourceCollection[MyResource]):\n"
                    "           meta: Optional[PaginationMeta] # or meta: PaginationMeta | None\n"
                    "    3. Remove the 'meta' attribute from your ResourceCollection subclass if it's not needed.\n"
                    "\n\n"
                )

            if len(data) == 0 or isinstance(data[0], dict):
                items = data or []
            else:
                items = [
                    self.__resource_cls__.from_model(model, with_relationships)
                    for model in data
                ]

            super().__init__(
                data=items,
                meta=None,
                **kwargs,
            )


class ResourceCollection(BaseCollection[ResourceType]):
    def __init__(self, items: ItemsType[ResourceType], /, **kwargs: Any) -> None:
        kwargs["data"] = items
        super().__init__(**kwargs)

    @model_serializer
    def _serialize(self):
        omit_if_none_fields = ["meta"]
        return {k: v for k, v in self if k not in omit_if_none_fields or v is not None}
