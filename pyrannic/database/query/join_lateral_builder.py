from pyrannic.contracts.database import (
    JoinLateralBuilderInterface,
)
from pyrannic.database.query.join_builder import JoinBuilder


class JoinLateralBuilder(JoinBuilder, JoinLateralBuilderInterface):
    """Implementation of the JoinLateralBuilderInterface for building lateral JOIN clauses."""
