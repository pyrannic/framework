from pydantic import Field
from pyrannic.auth.user_providers_config import UserProvidersConfig

from pyrannic import Configuration
from pyrannic.auth.guards_config import GuardsConfig


class AuthConfig(Configuration):
    guard: str = Field("web")
    """This value determines the default authentication guard for your application."""

    guards: GuardsConfig = Field(default=GuardsConfig())
    providers: UserProvidersConfig = Field(default=UserProvidersConfig())
