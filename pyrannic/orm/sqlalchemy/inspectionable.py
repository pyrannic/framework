from typing import Any

from sqlalchemy import inspect
from sqlalchemy.ext.hybrid import hybrid_method, hybrid_property
from sqlalchemy.orm import DeclarativeBase, MapperProperty, RelationshipProperty


class classproperty(object):
    """
    @property for @classmethod
    taken from http://stackoverflow.com/a/13624858
    """

    def __init__(self, fget: Any):
        self.fget = fget

    def __get__(self, owner_self: Any, owner_cls: Any) -> Any:
        return self.fget(owner_cls)


class Inspectionable(DeclarativeBase):
    @classproperty
    def properties(self) -> list[str]:
        return [item[0] for item in vars(self).items() if isinstance(item[1], property)]

    @classproperty
    def columns(self) -> list[str]:
        return inspect(self).columns.keys()  # type: ignore

    @classproperty
    def primary_keys_full(self) -> list[MapperProperty[Any]]:
        """Get primary key properties for a SQLAlchemy cls.
        Taken from marshmallow_sqlalchemy
        """
        mapper = self.__mapper__
        return [mapper.get_property_by_column(column) for column in mapper.primary_key]

    @classproperty
    def primary_keys(self):
        return [pk.key for pk in self.primary_keys_full]

    @classproperty
    def relations(self) -> list[str]:
        """Return a `list` of relationship names or the given model"""
        return [
            c.key for c in self.__mapper__.attrs if isinstance(c, RelationshipProperty)
        ]

    @classproperty
    def settable_relations(self):
        """Return a `list` of relationship names or the given model"""
        return [
            r for r in self.relations if getattr(self, r).property.viewonly is False
        ]

    @classproperty
    def hybrid_properties(self):
        items = inspect(self).all_orm_descriptors  # type: ignore
        return [item.__name__ for item in items if isinstance(item, hybrid_property)]  # type: ignore

    @classproperty
    def hybrid_methods_full(self):
        items = inspect(self).all_orm_descriptors  # type: ignore

        return {
            item.func.__name__: item
            for item in items  # type: ignore
            if type(item) is hybrid_method[Any, Any]  # type: ignore
        }

    @classproperty
    def hybrid_methods(self):
        return list(self.hybrid_methods_full.keys())
