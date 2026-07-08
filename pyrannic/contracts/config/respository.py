from abc import ABC, abstractmethod
from typing import Any

from annotated_types import T


class ConfigRepositoryInterface(ABC):
    @abstractmethod
    def has(self, name: str) -> bool:
        """Determine if the given configuration value exists."""

    @abstractmethod
    def get(self, name: str, default: Any | None = None) -> object | None:
        """Get the specified configuration value."""

    @abstractmethod
    def all(self) -> dict[str, Any]:
        """Get all of the configuration items for the application."""

    @abstractmethod
    def set(self, name: str, value: Any) -> None:
        """Set a given configuration value."""

    @abstractmethod
    def optional_string(self, name: str, default: str | None = None) -> str | None:
        """Get the specified configuration value as a string."""

    @abstractmethod
    def optional_integer(self, name: str, default: int | None = None) -> int | None:
        """Get the specified configuration value as an integer."""

    @abstractmethod
    def optional_float(self, name: str, default: float | None = None) -> float | None:
        """Get the specified configuration value as a float."""

    @abstractmethod
    def optional_boolean(self, name: str, default: bool | None = None) -> bool | None:
        """Get the specified configuration value as a boolean."""

    @abstractmethod
    def optional_list(
        self,
        name: str,
        default: list[T] | None = None,
    ) -> list[T] | None:
        """Get the specified configuration value as a list."""

    @abstractmethod
    def string(self, name: str, default: str = "") -> str:
        """Get the specified configuration value as a string."""

    @abstractmethod
    def integer(self, name: str, default: int = 0) -> int:
        """Get the specified configuration value as an integer."""

    @abstractmethod
    def float(self, name: str, default: float = 0.0) -> float:
        """Get the specified configuration value as a float."""

    @abstractmethod
    def boolean(self, name: str, default: bool = False) -> bool:
        """Get the specified configuration value as a boolean."""

    @abstractmethod
    def list(self, name: str, default: list[T] = []) -> list[T]:
        """Get the specified configuration value as a list."""
