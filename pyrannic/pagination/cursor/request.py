from pydantic import BaseModel, Field


class PaginationRequest(BaseModel):
    """
    This class is a trait/mixin to use in an actual request implementation to add cursor-based pagination support.

    The class adds the following attributes to the request:

        - page: Indicate the cursor position from which to start fetching the next set of items.
        - per_page: Tell us how many items there are in each page.
    """

    page: str | None = Field(
        default=None,
        description="Cursor for fetching the next set of items",
    )
    per_page: int = Field(default=15, ge=1, description="Number of items per page")
