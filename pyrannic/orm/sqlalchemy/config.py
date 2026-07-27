from pydantic import Field

from pyrannic import Configuration


class SQLAlchemyConfig(Configuration):
    asyncio: bool = Field(default=False)
    """Whether to use SQLAlchemy async engine for connections."""
