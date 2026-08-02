from typing import Any, Generic, Sequence, TypeAlias, TypeVar, Union, cast

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
        self._infer_resource_cls_if_needed()

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
                class_name = self.__class__.__name__

                raise RuntimeError(
                    "\n\n"
                    f"The 'meta' attribute is defined as required in your {class_name} class.\n"
                    "To fix this exception you have three options:\n"
                    "\n"
                    "    1. Instead of providing your items collection as a list, use a PaginatorInterface to provide the items.\n"
                    "       If you are using a repository to fetch your items, you can use the 'paginate' method of your repository\n"
                    f"       to get a paginator and pass it to your {class_name} directly:\n"
                    "\n"
                    f"          {class_name}(your_repository.paginate())\n"
                    "\n"
                    f"    2. Make the 'meta' attribute optional in your {class_name} class. E.g.:\n"
                    "\n"
                    f"       class {class_name}(ResourceCollection[MyResource]):\n"
                    f"           meta: Optional[PaginationMeta] # or meta: PaginationMeta | None\n"
                    "\n"
                    f"    3. Remove the 'meta' attribute from your {class_name} class if it's not needed.\n"
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

    def _infer_resource_cls_if_needed(self) -> None:
        """Infer the resource class if it is not set yet."""
        resource_cls = None

        if not hasattr(self, "__resource_cls__"):
            resource_cls = get_generic_type(self)
        else:
            resource_cls = self.__resource_cls__

        assert resource_cls is not None, (
            "Resource class must be set before initializing ResourceCollection"
        )

        self.__resource_cls__ = cast(type[ResourceType], resource_cls)


class ResourceCollection(BaseCollection[ResourceType]):
    def __init__(self, items: ItemsType[ResourceType], /, **kwargs: Any) -> None:
        kwargs["data"] = items
        super().__init__(**kwargs)

    @model_serializer
    def _serialize(self):
        omit_if_none_fields = ["meta"]
        return {k: v for k, v in self if k not in omit_if_none_fields or v is not None}
