from pydantic import Field

from pyrannic import Configuration, GuardsConfig, UserProvidersConfig


class AuthConfig(Configuration):
    guard: str = Field("bearer")
    guards: GuardsConfig = Field(default=GuardsConfig())
    providers: UserProvidersConfig = Field(default=UserProvidersConfig())
