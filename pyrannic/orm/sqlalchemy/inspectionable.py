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
    def properties(cls) -> list[str]:
        return [item[0] for item in vars(cls).items() if isinstance(item[1], property)]

    @classproperty
    def columns(cls) -> list[str]:
        return inspect(cls).columns.keys()  # type: ignore

    @classproperty
    def primary_keys_full(cls) -> list[MapperProperty[Any]]:
        """Get primary key properties for a SQLAlchemy cls.
        Taken from marshmallow_sqlalchemy
        """
        mapper = cls.__mapper__
        return [mapper.get_property_by_column(column) for column in mapper.primary_key]

    @classproperty
    def primary_keys(cls):
        return [pk.key for pk in cls.primary_keys_full]

    @classproperty
    def relations(cls):
        """Return a `list` of relationship names or the given model"""
        return [
            c.key for c in cls.__mapper__.attrs if isinstance(c, RelationshipProperty)
        ]

    @classproperty
    def settable_relations(cls):
        """Return a `list` of relationship names or the given model"""
        return [r for r in cls.relations if getattr(cls, r).property.viewonly is False]

    @classproperty
    def hybrid_properties(cls):
        items = inspect(cls).all_orm_descriptors  # type: ignore
        return [item.__name__ for item in items if isinstance(item, hybrid_property)]  # type: ignore

    @classproperty
    def hybrid_methods_full(cls):
        items = inspect(cls).all_orm_descriptors  # type: ignore

        return {
            item.func.__name__: item
            for item in items  # type: ignore
            if type(item) is hybrid_method[Any, Any]  # type: ignore
        }

    @classproperty
    def hybrid_methods(cls):
        return list(cls.hybrid_methods_full.keys())
