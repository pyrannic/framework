from typing import Any, Iterable

from pyrannic.contracts.support.serializable import SerializableInterface
from pyrannic.orm.sqlalchemy.inspectionable import Inspectionable


class Serializable(Inspectionable, SerializableInterface):
    __abstract__ = True

    def to_dict(
        self,
        nested: bool = False,
        hybrid_attributes: bool = False,
        exclude: list[str] | None = None,
    ) -> dict[str, Any]:
        """Return dict object with model's data.

        :param nested: flag to return nested relationships' data if true
        :type: bool
        :param hybrid_attributes: flag to include hybrid attributes if true
        :type: bool
        :param exclude: an optional list of attribute names to exclude
        :type: list
        :return: dict
        """
        result = dict[str, Any]()
        columns: list[str] = self.columns + self.properties  # pyright: ignore[reportUnknownMemberType]

        if exclude is None:
            view_cols = columns
        else:
            view_cols = filter(lambda e: e not in exclude, columns)

        for key in view_cols:
            try:
                result[key] = getattr(self, key)
            except Exception as e:
                print(key, e)

        if hybrid_attributes:
            for key in self.hybrid_properties:
                result[key] = getattr(self, key)

        if nested:
            for key in self.relations:
                obj = getattr(self, key)

                if isinstance(obj, Serializable):
                    result[key] = obj.to_dict(hybrid_attributes=hybrid_attributes)
                elif isinstance(obj, Iterable):
                    result[key] = [
                        o.to_dict(hybrid_attributes=hybrid_attributes)
                        for o in obj  # type: ignore
                        if isinstance(o, Serializable)
                    ]

        return result
