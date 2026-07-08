from typing import Any, Optional

from pydantic import Field

from pyrannic import PaginationMeta, Resource, ResourceCollection
from pyrannic.http.resources import HasTimestamps, ItemsType, SoftDeletes


class Hero(Resource, HasTimestamps, SoftDeletes):
    id: str = Field(coerce_numbers_to_str=True)
    name: str = Field(
        description="The name of the hero, e.g., 'Superman', 'Batman'.",
    )

    description: Optional[str] = Field(
        default=None,
        description="The description of the hero, e.g., 'The Man of Steel', 'The Dark Knight'.",
    )


class HeroesCollection(ResourceCollection[Hero]):
    __resource_cls__ = Hero
    meta: PaginationMeta

    # NOTE: Needed to avoid static typing issues with the IDE.
    def __init__(self, items: ItemsType[Hero], /, **kwargs: Any) -> None:
        super().__init__(items, **kwargs)
