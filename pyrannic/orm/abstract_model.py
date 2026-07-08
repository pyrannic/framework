from pyrannic.contracts.orm.model import ModelInterface
from pyrannic.contracts.support.serializable import SerializableInterface
from pyrannic.support import inflect, string

_SUFFIXES_TO_REMOVE = ["Model", "Entity", "Schema", "Table"]


class AbstractModel(ModelInterface, SerializableInterface):
    __abstract__ = True

    @classmethod
    def tablename(cls) -> str:
        name = cls.__name__

        for suffix in _SUFFIXES_TO_REMOVE:
            if name.endswith(suffix):
                name = name.replace(suffix, "", 1)

        return inflect.pluralize(string.to_snake_case(name))
