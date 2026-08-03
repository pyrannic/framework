from pydantic import Field

from pyrannic import Configuration
from pyrannic.auth.config.guards_config import GuardsConfig
from pyrannic.auth.config.user_providers_config import UserProvidersConfig


class AuthConfig(Configuration):
    guard: str = Field("bearer")
    """This determines the default authentication guard for your application."""

    guards: GuardsConfig = Field(default=GuardsConfig())
    providers: UserProvidersConfig = Field(default=UserProvidersConfig())
