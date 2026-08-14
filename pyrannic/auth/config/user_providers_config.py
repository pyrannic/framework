from pydantic import Field

from pyrannic.config.configuration import Configuration


class SQLAlchemyUserProviderConfig(Configuration):
    driver: str = Field(default="sqlalchemy")
    """The authentication driver to be used by the user provider."""

    model: str = Field(default="app.models.User")
    """The model class to be used by the user provider."""

    @property
    def env_prefix(self) -> str:
        return "AUTH_"


class UserProvidersConfig(Configuration):
    sqlalchemy: SQLAlchemyUserProviderConfig = Field(
        default_factory=lambda: SQLAlchemyUserProviderConfig()
    )
    """Configuration for the SQLAlchemy user provider."""
