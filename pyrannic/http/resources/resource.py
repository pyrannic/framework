from typing import Any, Self, cast

from pydantic import PrivateAttr

from pyrannic.contracts.http.resources.resource import ResourceInterface
from pyrannic.contracts.support.serializable import SerializableInterface


class Resource(ResourceInterface):
    _with_relationships: bool | list[str] = PrivateAttr(default=True)

    @classmethod
    def from_model(
        cls,
        model: SerializableInterface,
        with_relationships: bool | list[str] = True,
    ) -> Self:
        cls._with_relationships = with_relationships

        if isinstance(model, ResourceInterface):
            return cast(Self, model)

        return cls.model_validate(cls.model_to_dict(model))

    @classmethod
    def model_to_dict(cls, model: SerializableInterface) -> dict[str, Any]:
        return {
            **cls._attrs(model),
            **cls.__relationships(model),
        }

    @classmethod
    def __relationships(cls, model: SerializableInterface) -> dict[str, Any]:
        if not cls._with_relationships:
            relationships = {}
        else:
            all_relationships: dict[str, dict[str, Any]] = cls._relationships(model)

            if isinstance(cls._with_relationships, list):
                relationships = {
                    k: v
                    for k, v in all_relationships.items()
                    if k in cls._with_relationships
                }
            else:
                relationships = all_relationships

        return relationships

    def to_dict(
        self,
        nested: bool = False,
        hybrid_attributes: bool = False,
        exclude: list[str] | None = None,
    ) -> dict[str, Any]:
        return self.model_dump(exclude=set(exclude) if exclude else set())
