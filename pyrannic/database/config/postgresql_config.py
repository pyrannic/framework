from typing import Any

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

    sslmode: str = Field(default="prefer")
    """The SSL mode to use for the database connection."""

    url: str | None = Field(default=None)
    """The database connection URL. If provided, it will override the other connection parameters."""

    def to_dict(self) -> dict[str, Any]:
        data = super().to_dict()

        data["query"] = {
            "sslmode": self.sslmode,  # For psycopg2
            "ssl": self.sslmode,  # For asyncpg
        }

        return data
