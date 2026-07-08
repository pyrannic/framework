from datetime import datetime

from pyrannic.contracts.orm.model import ModelInterface


class SoftDeletesInterface(ModelInterface):
    def set_deleted_at(self, deleted_at: datetime | None) -> None:
        raise NotImplementedError

    @property
    def is_deleted(self) -> bool:
        raise NotImplementedError

    @classmethod
    def deleted_at_column(cls) -> str:
        raise NotImplementedError
