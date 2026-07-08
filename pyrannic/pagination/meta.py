from pydantic import BaseModel, Field, ValidationInfo, field_validator


class PaginationMeta(BaseModel):
    """
    Class to be used together with ResourceCollection class as its meta information.
    In this way, a collection response can have meta information such as total number of items, current page requested,
    number of items per page, etc.
    """

    current_page: int = Field(ge=1, description="Current page number")
    last_page: int = Field(ge=1, description="Last page number")
    per_page: int = Field(default=15, ge=1, description="Number of items per page")
    total: int = Field(ge=0, description="Total number of items")

    from_index: int = Field(
        ge=0,
        serialization_alias="from",
        description="Starting index of the items on the current page",
    )

    to_index: int = Field(
        ge=0,
        serialization_alias="to",
        description="Ending index of the items on the current page",
    )

    @field_validator("last_page")
    @classmethod
    def _validate_last_page(cls, value: int, info: ValidationInfo) -> int:
        if "current_page" in info.data and value < info.data["current_page"]:
            raise ValueError("last_page must be greater than or equal to current_page")
        return value

    def __repr__(self):
        return f"PaginationMeta(current_page={self.current_page!r}, last_page={self.last_page!r}, per_page={self.per_page!r}, total={self.total!r}, from_index={self.from_index!r}, to_index={self.to_index!r})"
