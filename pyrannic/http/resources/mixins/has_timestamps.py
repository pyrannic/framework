from datetime import datetime

from pydantic import BaseModel, Field, field_serializer

from pyrannic.support.datetime import encode_datetime_to_iso_8601_with_z_suffix


class HasTimestamp(BaseModel):
    created_at: datetime = Field()

    @field_serializer("created_at", when_used="json")
    def serialize_created_at(self, created_at: datetime):
        return encode_datetime_to_iso_8601_with_z_suffix(created_at)


class HasTimestamps(HasTimestamp):
    updated_at: datetime = Field()

    @field_serializer("updated_at", when_used="json")
    def serialize_updated_at(self, updated_at: datetime):
        return encode_datetime_to_iso_8601_with_z_suffix(updated_at)
