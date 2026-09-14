from pydantic import Field

from pyrannic.config.configuration import Configuration


class SQLAlchemyConfig(Configuration):
    asyncio: bool = Field(default=False)
    """Whether to use SQLAlchemy async engine for connections."""

    echo: bool = Field(default=False)
    """Whether to enable SQLAlchemy echo for logging SQL statements."""

    pool_size: int | None = Field(default=None)
    """The size of the SQLAlchemy connection pool."""

    pool_pre_ping: bool = Field(default=True)
    """Whether to enable SQLAlchemy's pool pre-ping feature."""

    max_overflow: int | None = Field(default=None)
    """The maximum number of connections that can be created beyond the pool_size."""

    future: bool = Field(default=True)
    """Whether to enable SQLAlchemy's future mode for lazy connections."""

    alembic: bool = Field(default=True)
    """Whether to run Alembic migrations after running the provided migration classes."""
