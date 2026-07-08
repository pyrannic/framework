from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from pyrannic.orm.sqlalchemy import HasTimestamps, Model, SoftDeletes


class Hero(Model, HasTimestamps, SoftDeletes):
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
        comment="Unique identifier for the hero; serves as the primary key.",
    )

    name: Mapped[str] = mapped_column(
        String(64),
        comment="The name of the hero, e.g., 'Superman', 'Batman'.",
    )

    description: Mapped[str] = mapped_column(
        String(255),
        comment="The description of the hero, e.g., 'The Man of Steel', 'The Dark Knight'.",
    )
