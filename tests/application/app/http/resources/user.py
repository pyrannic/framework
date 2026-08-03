from typing import Any

from pydantic import Field

from pyrannic import PaginationMeta, Resource, ResourceCollection
from pyrannic.http.resources import HasTimestamps, ItemsType


class User(Resource, HasTimestamps):
    id: str = Field(coerce_numbers_to_str=True)
    name: str = Field(
        description="The name of the user, e.g., 'John Doe', 'Jane Smith'.",
    )

    email: str = Field(
        max_length=255,
        description="The email of the user, e.g., 'john.doe@example.com', 'jane.smith@example.com'.",
    )


class UsersCollection(ResourceCollection[User]):
    meta: PaginationMeta

    # NOTE: Needed to avoid static typing issues with the IDE.
    def __init__(self, items: ItemsType[User], /, **kwargs: Any) -> None:
        super().__init__(items, **kwargs)
