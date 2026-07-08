from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer

from pyrannic.orm.sqlalchemy import Model


class BarModel(Model):
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
        comment="Unique identifier for the hero; serves as the primary key.",
    )
