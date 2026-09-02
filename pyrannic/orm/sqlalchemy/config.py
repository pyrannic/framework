from pydantic import Field

from pyrannic.config.configuration import Configuration


class SQLAlchemyConfig(Configuration):
    asyncio: bool = Field(default=False)
    """Whether to use SQLAlchemy async engine for connections."""

    alembic: bool = Field(default=True)
    """Whether to run Alembic migrations after running the provided migration classes."""
