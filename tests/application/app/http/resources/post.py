from typing import Any

from pydantic import Field

from pyrannic import PaginationMeta, Resource, ResourceCollection
from pyrannic.http.resources import HasTimestamps, ItemsType


class Post(Resource, HasTimestamps):
    id: str = Field(coerce_numbers_to_str=True)
    title: str = Field(
        description="The title of the post, e.g., 'My First Post', 'A Day in the Life'.",
    )
    content: str = Field(
        description="The content of the post, e.g., 'This is my first post!', 'Today I went to the park.'.",
    )


class PostsCollection(ResourceCollection[Post]):
    meta: PaginationMeta

    # NOTE: Needed to avoid static typing issues with the IDE.
    def __init__(self, items: ItemsType[Post], /, **kwargs: Any) -> None:
        super().__init__(items, **kwargs)
