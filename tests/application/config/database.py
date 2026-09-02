from pydantic import Field

from pyrannic import DatabaseConfig as Configuration
from pyrannic.database import ConnectionsConfig


class DatabaseConfig(Configuration):
    connection: str = Field(default="sqlite")
    """The name of the database connection to use."""

    connections: ConnectionsConfig = Field(default_factory=ConnectionsConfig)
    """Configuration for database connections."""
