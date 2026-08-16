from fastapi.security import HTTPBearer
from fastapi.security.base import SecurityBase
from pydantic import Field

from pyrannic.config.configuration import Configuration


class GuardConfig(Configuration):
    driver: str = Field(default="bearer")
    """The authentication driver to be used by the guard."""

    security_model: SecurityBase = Field(default_factory=HTTPBearer)
    """The security model to be used by the guard. If not set, the default security model for the driver will be used."""


class JwtGuardConfig(GuardConfig):
    driver: str = Field(default="jwt")
    """The authentication driver to be used by the guard."""

    security_model: SecurityBase = Field(default_factory=HTTPBearer)
    """The security model to be used by the guard. If not set, the default security model for the driver will be used."""

    jwks_url: str | None = Field(default=None)
    """
    The URL to the JWKS endpoint for JWT validation.
    If not set, JWT validation will not be performed.
    """

    algorithms: list[str] = Field(default_factory=lambda: ["RS256"])
    """
    The list of algorithms to be used for JWT validation.
    If not set, the default algorithm will be used.
    """

    require: list[str] = Field(default_factory=lambda: [])
    """The list of claims that must be present in the JWT."""

    verify: list[str] = Field(
        default_factory=lambda: ["exp", "iss", "aud", "sub", "nbf", "iat", "jti"]
    )
    """The list of claims that must be verified in the JWT."""

    verify_signature: bool = Field(default=True)
    """Whether to verify the JWT signature."""

    strict_audience: bool = Field(default=True)
    """Check that the aud claim is a single value (not a list), and matches audience exactly."""

    audience: str | None = Field(default=None)
    """The expected audience claim for JWT validation."""

    subject: str | None = Field(default=None)
    """The expected subject claim for JWT validation."""

    issuer: str | None = Field(default=None)
    """The expected issuer claim for JWT validation."""

    leeway: float = Field(default=0)
    """
    The amount of leeway (in seconds) to allow when validating the expiration time of a JWT.
    """

    @property
    def env_prefix(self) -> str:
        return "JWT_"


class GuardsConfig(Configuration):
    bearer: GuardConfig = Field(default_factory=GuardConfig)
    """Configuration for the bearer guard."""

    jwt: JwtGuardConfig = Field(default_factory=JwtGuardConfig)
    """Configuration for the JWT guard."""
