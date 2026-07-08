from typing import Any


class SerializableInterface:
    __abstract__ = True

    def to_dict(self, *args: Any, **kwargs: Any) -> dict[str, Any]:
        return {}
