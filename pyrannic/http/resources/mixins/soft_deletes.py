from datetime import datetime

from pydantic import BaseModel, Field, field_serializer

from pyrannic.support.datetime import encode_datetime_to_iso_8601_with_z_suffix


class SoftDeletes(BaseModel):
    deleted_at: datetime | None = Field(default=None)

    @field_serializer("deleted_at", when_used="json")
    def serialize_deleted_at(self, deleted_at: datetime | None):
        return (
            None
            if deleted_at is None
            else encode_datetime_to_iso_8601_with_z_suffix(deleted_at)
        )
