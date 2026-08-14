from pydantic import Field

from pyrannic.config.configuration import Configuration
from pyrannic.orm.sqlalchemy.config import SQLAlchemyConfig


class DriversConfig(Configuration):
    sqlalchemy: SQLAlchemyConfig = Field(default_factory=lambda: SQLAlchemyConfig())
    """Configuration for SQLAlchemy driver."""
