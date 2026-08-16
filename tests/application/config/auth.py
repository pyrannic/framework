from pydantic import Field

from pyrannic import Configuration, GuardsConfig, UserProvidersConfig


class AuthConfig(Configuration):
    guard: str = Field("jwt")
    """This determines the default authentication guard for your application."""

    guards: GuardsConfig = Field(default_factory=GuardsConfig)
    """
    This configuration allows you to define the authentication guards for your application.

    Each guard is configured with a user provider, which determines how users are retrieved
    from your database or other persistent storage systems.
    """

    providers: UserProvidersConfig = Field(default_factory=UserProvidersConfig)
    """
    Each authentication guard relies on a user provider to determine how users
    are retrieved from your database or application storage.
    
    If your application utilizes multiple user tables or models, you can configure
    distinct providers for each one. These configured providers can then be assigned
    to any additional authentication guards you establish.
    """
