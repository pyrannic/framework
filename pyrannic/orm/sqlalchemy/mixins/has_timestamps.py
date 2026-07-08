from datetime import datetime
from typing import Any

from sqlalchemy import DateTime, func
from sqlalchemy.orm import Mapped, declared_attr, mapped_column

from pyrannic.contracts.orm.mixins.has_timestamps import (
    HasTimestampInterface,
    HasTimestampsInterface,
)
from pyrannic.support.datetime import get_current_utc_datetime


class HasTimestamp(HasTimestampInterface):
    __created_at_column_name__ = "created_at"

    def set_created_at(self, created_at: datetime | None) -> None:
        self.created_at = created_at

    @declared_attr
    def created_at(self) -> Mapped[datetime]:
        return mapped_column(
            DateTime(timezone=True),
            server_default=func.now(),
            name=self.__created_at_column_name__,
        )

    def __pre_init__(self, **kwargs: Any):
        super().__pre_init__(**kwargs)
        self.created_at = (
            kwargs.get(self.__created_at_column_name__) or get_current_utc_datetime()
        )


class HasTimestamps(HasTimestamp, HasTimestampsInterface):
    __updated_at_column_name__ = "updated_at"

    def set_updated_at(self, updated_at: datetime | None) -> None:
        self.updated_at = updated_at

    @declared_attr
    def updated_at(self) -> Mapped[datetime]:
        return mapped_column(
            DateTime(timezone=True),
            server_default=func.now(),
            onupdate=func.current_timestamp(),
            name=self.__updated_at_column_name__,
        )

    def __pre_init__(self, **kwargs: Any):
        super().__pre_init__(**kwargs)
        self.updated_at = kwargs.get(self.__updated_at_column_name__) or self.created_at
