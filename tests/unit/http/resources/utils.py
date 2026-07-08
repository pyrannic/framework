from datetime import datetime
from typing import Any

from pyrannic.contracts.support.serializable import SerializableInterface
from pyrannic.http.resources.collection import ItemsType, ResourceCollection
from pyrannic.http.resources.mixins.has_timestamps import HasTimestamp, HasTimestamps
from pyrannic.http.resources.mixins.soft_deletes import SoftDeletes
from pyrannic.http.resources.resource import Resource


class HasTimestampResource(Resource, HasTimestamp):
    id: int
    name: str


class HasTimestampsResource(Resource, HasTimestamps):
    id: int
    name: str


class SoftDeletesResource(Resource, SoftDeletes):
    id: int
    name: str


class FooResource(Resource, HasTimestamps, SoftDeletes):
    id: int
    name: str


class FooResourceWithRelationships(Resource, HasTimestamps, SoftDeletes):
    id: int
    name: str

    @classmethod
    def _relationships(cls, model: SerializableInterface) -> dict[str, Any]:

        print("_relationships called with model:", getattr(model, "children", []))

        return {
            "children": [
                FooResourceWithRelationships.from_model(child)
                for child in getattr(model, "children", [])
            ],
        }


class FooModel(SerializableInterface):
    def __init__(
        self,
        id: int,
        name: str,
        created_at: datetime,
        updated_at: datetime,
        deleted_at: datetime | None = None,
        children: list["FooModel"] | None = None,
    ) -> None:
        self.id = id
        self.name = name
        self.created_at = created_at
        self.updated_at = updated_at
        self.deleted_at = deleted_at
        self.children = children or []

    def to_dict(self, *args: Any, **kwargs: Any) -> dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "deleted_at": self.deleted_at,
        }


class FooCollection(ResourceCollection[FooResource]):
    __resource_cls__ = FooResource

    def __init__(self, items: ItemsType[FooResource], /, **kwargs: Any) -> None:
        super().__init__(items, **kwargs)


class BarCollection(ResourceCollection[FooResource]):
    def __init__(self, items: ItemsType[FooResource], /, **kwargs: Any) -> None:
        super().__init__(items, **kwargs)
