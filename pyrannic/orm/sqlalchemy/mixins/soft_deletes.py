from datetime import datetime

from sqlalchemy import ColumnElement, DateTime
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, declared_attr, mapped_column

from pyrannic.contracts.orm.mixins.soft_deletes import SoftDeletesInterface


class SoftDeletes(SoftDeletesInterface):
    __deleted_at_column_name__ = "deleted_at"

    @declared_attr
    def deleted_at(self) -> Mapped[datetime | None]:
        return mapped_column(
            DateTime(timezone=True),
            nullable=True,
            comment="The date when the model has been deleted; NULL if not deleted.",
            name=self.__deleted_at_column_name__,
        )

    def set_deleted_at(self, deleted_at: datetime | None) -> None:
        self.deleted_at = deleted_at

    @hybrid_property
    def is_deleted(self) -> bool:  # type: ignore
        return self.deleted_at is not None

    @is_deleted.inplace.expression
    @classmethod
    def _is_deleted_expression(cls) -> ColumnElement[bool]:
        return cls.deleted_at.isnot(None)

    @classmethod
    def deleted_at_column(cls) -> str:
        return cls.__deleted_at_column_name__
