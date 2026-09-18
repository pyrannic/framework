from pydantic import Field
from sqlalchemy.pool import StaticPool

from pyrannic import Configuration
from pyrannic.orm import DriversConfig
from pyrannic.orm.sqlalchemy import SQLAlchemyConfig


class OrmConfig(Configuration):
    default: str = Field(default="sqlalchemy")
    """The default ORM to use."""

    drivers: DriversConfig = Field(
        default_factory=lambda: DriversConfig(
            sqlalchemy=SQLAlchemyConfig(poolclass=StaticPool)
        )
    )
    """The configuration for the ORM connections."""
