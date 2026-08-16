from pydantic import Field

from pyrannic import Configuration
from pyrannic.orm import DriversConfig


class OrmConfig(Configuration):
    default: str = Field(default="sqlalchemy")
    """The default ORM to use."""

    drivers: DriversConfig = Field(default_factory=DriversConfig)
    """The configuration for the ORM connections."""
