from pydantic import Field

from pyrannic import Configuration


class GuardConfig(Configuration):
    driver: str = Field(default="web")
    """The authentication driver to be used by the guard."""

    provider: str = Field(default="users")
    """The user provider to be used by the guard."""


class GuardsConfig(Configuration):
    web: GuardConfig = Field(default=GuardConfig())
    """Configuration for the web guard."""
