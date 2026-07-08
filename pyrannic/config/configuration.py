import json
from typing import Any

from pydantic.fields import FieldInfo

from pydantic_settings import (
    BaseSettings,
    DotEnvSettingsSource,
    EnvSettingsSource,
    PydanticBaseSettingsSource,
)
from pyrannic.contracts.config.configuration import ConfigurationInterface


class CustomEnvSettingsSource(EnvSettingsSource):
    def prepare_field_value(
        self,
        field_name: str,
        field: FieldInfo,
        value: Any,
        value_is_complex: bool,
    ) -> Any:
        if isinstance(value, str):
            if field.annotation == list[str]:
                return value.split(",")
            elif field.annotation == list[int]:
                return [int(v) for v in value.split(",")]

        return json.loads(value) if value_is_complex else value


class CustomDotEnvSettingsSource(DotEnvSettingsSource, CustomEnvSettingsSource):
    pass


class Configuration(ConfigurationInterface, BaseSettings):
    def __init__(self, **kwargs: Any) -> None:
        super().__init__(
            _case_sensitive=False,
            _env_prefix=self.env_prefix,
            **kwargs,
        )

    @property
    def config_key(self) -> str:
        return self.__class__.__name__.replace("Config", "").lower()

    @property
    def env_prefix(self) -> str:
        return f"{self.config_key.upper()}_"

    def to_dict(self) -> dict[str, Any]:
        return self.model_dump()

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        if isinstance(env_settings, EnvSettingsSource):
            env_settings = CustomEnvSettingsSource(
                cls,
                case_sensitive=env_settings.case_sensitive,
                env_prefix=env_settings.env_prefix,
                env_prefix_target=env_settings.env_prefix_target,  # type: ignore
                env_nested_delimiter=env_settings.env_nested_delimiter,
                env_nested_max_split=env_settings.env_nested_max_split,
                env_ignore_empty=env_settings.env_ignore_empty,
                env_parse_none_str=env_settings.env_parse_none_str,
                env_parse_enums=env_settings.env_parse_enums,
            )

        if isinstance(dotenv_settings, DotEnvSettingsSource):
            dotenv_settings = CustomDotEnvSettingsSource(
                cls,
                env_file=dotenv_settings.env_file,
                env_file_encoding=dotenv_settings.env_file_encoding,
                case_sensitive=dotenv_settings.case_sensitive,
                env_prefix=dotenv_settings.env_prefix,
                env_prefix_target=dotenv_settings.env_prefix_target,  # type: ignore
                env_nested_delimiter=dotenv_settings.env_nested_delimiter,
                env_nested_max_split=dotenv_settings.env_nested_max_split,
                env_ignore_empty=dotenv_settings.env_ignore_empty,
                env_parse_none_str=dotenv_settings.env_parse_none_str,
                env_parse_enums=dotenv_settings.env_parse_enums,
            )

        return (
            init_settings,
            env_settings,
            dotenv_settings,
            file_secret_settings,
        )
