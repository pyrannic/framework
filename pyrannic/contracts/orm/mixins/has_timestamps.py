from datetime import datetime

from pyrannic.contracts.orm.model import ModelInterface


class HasTimestampInterface(ModelInterface):
    def set_created_at(self, created_at: datetime | None) -> None:
        raise NotImplementedError


class HasTimestampsInterface(HasTimestampInterface):
    def set_updated_at(self, updated_at: datetime | None) -> None:
        raise NotImplementedError
