from abc import abstractmethod
from typing import Any


class ModelInterface:
    def __pre_init__(self, **kwargs: Any):
        pass

    def __post_init__(self, **kwargs: Any):
        pass

    @classmethod
    @abstractmethod
    def primary_key_column(cls) -> Any:
        pass

    @property
    @abstractmethod
    def primary_key_value(self) -> Any:
        pass

    @classmethod
    @abstractmethod
    def tablename(cls) -> str:
        """Return the table name for the model."""

    @classmethod
    @abstractmethod
    def columns(cls) -> list[str]:
        """Return the columns for the model."""
