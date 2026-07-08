from typing import Any


class ConfigurationInterface:
    @property
    def config_key(self) -> str:
        raise NotImplementedError("Subclasses must implement config_key property")

    def to_dict(self) -> dict[str, Any]:
        raise NotImplementedError("Subclasses must implement to_dict method")
