from pydantic import Field

from pyrannic import Configuration


class SqlalchemyConfig(Configuration):
    asyncio: bool = Field(default=False)
    """Whether to use SQLAlchemy async engine for connections."""


class ServicesConfig(Configuration):
    sqlalchemy: SqlalchemyConfig = Field(default=SqlalchemyConfig())
    """Configuration for SQLAlchemy."""
