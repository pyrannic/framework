from pydantic import Field

from pyrannic.database.config.base_config import DatabaseConfig


class SqliteConfig(DatabaseConfig):
    driver: str = Field(default="sqlite")
    """The database driver to use."""

    database: str = Field(default="database/database.sqlite")
    """File path for SQLite database."""

    url: str | None = Field(default=None)
    """The database connection URL. If provided, it will override the other connection parameters."""
