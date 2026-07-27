from pydantic import Field

from pyrannic import Configuration
from pyrannic.orm.sqlalchemy.config import SQLAlchemyConfig


class DriversConfig(Configuration):
    sqlalchemy: SQLAlchemyConfig = Field(default=SQLAlchemyConfig())
    """Configuration for SQLAlchemy driver."""
