from pydantic import Field

from pyrannic.config.configuration import Configuration
from pyrannic.database.config.postgresql_config import PostgresqlConfig
from pyrannic.database.config.sqlite_config import SqliteConfig


class ConnectionsConfig(Configuration):
    sqlite: SqliteConfig = Field(default_factory=SqliteConfig)
    """Configuration for SQLite database connection."""

    postgresql: PostgresqlConfig = Field(default_factory=PostgresqlConfig)
    """Configuration for PostgreSQL database connection."""
