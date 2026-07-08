import os
from pyranninc.contracts import ConfigurationInterface


class AppConfig(ConfigurationInterface):
    @property
    def config_key(self) -> str:
        return "app"

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": os.environ.get("app_name"),
            "env": os.environ.get("app_env"),
            "debug": True,
        }
