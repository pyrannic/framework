from pydantic import Field

from pyrannic.database.config.base_config import DatabaseConfig


class PostgresqlConfig(DatabaseConfig):
    driver: str = Field(default="postgresql")
    """The database driver to use."""

    host: str = Field(default="localhost")
    """The database host to connect to."""

    port: int = Field(default=5432)
    """The database port to connect to."""

    database: str = Field(default="")
    """The name of the database to connect to."""

    username: str = Field(default="")
    """The username to use for database authentication."""

    password: str = Field(default="")
    """The password to use for database authentication."""

    url: str | None = Field(default=None)
    """The database connection URL. If provided, it will override the other connection parameters."""
