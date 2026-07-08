from pydantic import Field

from pyrannic import Configuration


class DBConfig(Configuration):
    @property
    def env_prefix(self) -> str:
        return "DB_"


class SqliteConfig(DBConfig):
    driver: str = "sqlite"
    """The database driver to use."""

    url: str | None = Field(default=None)

    database: str = Field(default="database/database.sqlite")
    """File path for SQLite database."""


class ConnectionsConfig(DBConfig):
    sqlite: SqliteConfig = Field(default=SqliteConfig())
    """Configuration for SQLite database connection."""


class MigrationsConfig(DBConfig):
    alembic: bool = Field(default=True)
    """Whether to run Alembic migrations after running the provided migration classes."""


class DatabaseConfig(DBConfig):
    connections: ConnectionsConfig = Field(default=ConnectionsConfig())
    """Configuration for database connections."""

    migrations: MigrationsConfig = Field(default=MigrationsConfig())
    """Configuration for database migrations."""
