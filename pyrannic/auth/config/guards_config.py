from fastapi.security import HTTPBearer
from fastapi.security.base import SecurityBase
from pydantic import Field

from pyrannic.config.configuration import Configuration


class GuardConfig(Configuration):
    driver: str = Field(default="bearer")
    """The authentication driver to be used by the guard."""

    provider: str = Field(default="sqlalchemy")
    """The user provider to be used by the guard."""

    security_model: SecurityBase = Field(default=HTTPBearer())
    """The security model to be used by the guard. If not set, the default security model for the driver will be used."""


class GuardsConfig(Configuration):
    bearer: GuardConfig = Field(default=GuardConfig())
    """Configuration for the bearer guard."""
