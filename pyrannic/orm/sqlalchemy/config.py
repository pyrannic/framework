from pydantic import Field

from pyrannic.config.configuration import Configuration


class SQLAlchemyConfig(Configuration):
    asyncio: bool = Field(default=False)
    """Whether to use SQLAlchemy async engine for connections."""
