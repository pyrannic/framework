from typing import Any

from annotated_types import T

from pyrannic.contracts.config.respository import ConfigRepositoryInterface
from pyrannic.support.collections.dot_dict import get, has, set


class ConfigRepository(ConfigRepositoryInterface):
    _items: dict[str, Any] = {}

    def __init__(self, items: dict[str, Any] = dict()) -> None:
        self._items = items

    def __getattr__(self, name: str) -> Any:
        if self.has(name):
            return self.get(name)

        raise AttributeError(f"{self.__class__.__name__!r} has no attribute {name!r}")

    def __setattr__(self, name: str, value: Any) -> None:
        if name == "_items":
            super().__setattr__(name, value)
        else:
            self.set(name, value)

    def has(self, name: str) -> bool:
        return has(self._items, name)

    def get(self, name: str, default: Any | None = None) -> Any | None:
        return get(self._items, name, default)

    def all(self) -> dict[str, Any]:
        return dict(self._items)

    def set(self, name: str, value: Any) -> None:
        set(self._items, name, value)

    def optional_string(self, name: str, default: str | None = None) -> str | None:
        value = self.get(name, default)
        return str(value) if value is not None else default

    def optional_integer(self, name: str, default: int | None = None) -> int | None:
        value = self.get(name, default)

        try:
            return int(value) if value is not None else default
        except (ValueError, TypeError):
            return default

    def optional_float(self, name: str, default: float | None = None) -> float | None:
        value = self.get(name, default)

        try:
            return float(value) if value is not None else default
        except (ValueError, TypeError):
            return default

    def optional_boolean(self, name: str, default: bool | None = None) -> bool | None:
        value = self.get(name, default)

        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            return value.lower() in ["true", "1", "yes"]
        if isinstance(value, (int, float)):
            return value != 0

        return default

    def optional_list(
        self,
        name: str,
        default: list[T] | None = None,
    ) -> list[T] | None:
        value = self.get(name, default)
        return list(value) if value is not None else default

    def string(self, name: str, default: str = "") -> str:
        return self.optional_string(name, default) or default

    def integer(self, name: str, default: int = 0) -> int:
        return self.optional_integer(name, default) or default

    def float(self, name: str, default: float = 0.0) -> float:
        return self.optional_float(name, default) or default

    def boolean(self, name: str, default: bool = False) -> bool:
        return self.optional_boolean(name, default) or default

    def list(self, name: str, default: list[T] = []) -> list[T]:
        return self.optional_list(name, default) or default
