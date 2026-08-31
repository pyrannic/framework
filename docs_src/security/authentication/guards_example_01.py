from pydantic import Field

from pyrannic import Configuration


class AuthConfig(Configuration):
    guard: str = Field("bearer")
    """This determines the default authentication guard for your application."""
