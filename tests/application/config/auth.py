from pydantic import Field

from pyrannic import Configuration
from pyrannic.auth.guards_config import GuardsConfig
from pyrannic.auth.user_providers_config import UserProvidersConfig


class AuthConfig(Configuration):
    guard: str = Field("bearer")
    """This determines the default authentication guard for your application."""

    guards: GuardsConfig = Field(default=GuardsConfig())
    providers: UserProvidersConfig = Field(default=UserProvidersConfig())
