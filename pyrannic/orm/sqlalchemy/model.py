from typing import Any

from sqlalchemy import ColumnExpressionArgument, inspect
from sqlalchemy.orm import DeclarativeBase, declared_attr

from pyrannic.orm.abstract_model import AbstractModel
from pyrannic.orm.sqlalchemy.serializable import Serializable


class BaseModel(DeclarativeBase):
    __abstract__ = True


class Model(BaseModel, AbstractModel, Serializable):
    __abstract__ = True

    def __init__(self, **kwargs: Any):
        self.__pre_init__(**kwargs)
        self.registry.constructor(self, **kwargs)
        self.__post_init__(**kwargs)

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.tablename()

    @classmethod
    def primary_key_column(cls) -> ColumnExpressionArgument[Any]:
        return list(cls.__table__.primary_key.columns)[0]  # type: ignore

    @property
    def primary_key_value(self) -> Any:
        pk_column = self.primary_key_column()
        return getattr(self, pk_column.name)  # type: ignore

    def is_dirty(self, *attrs: str) -> bool:
        state = inspect(self)
        len_attrs = len(attrs)

        for attr in state.attrs:
            if (len_attrs == 0 or attr.key in attrs) and attr.history.has_changes():
                return True

        return False

    def is_clean(self, *attrs: str) -> bool:
        return not self.is_dirty(*attrs)
