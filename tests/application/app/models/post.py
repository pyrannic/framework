from sqlalchemy import Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from pyrannic.orm.sqlalchemy import HasTimestamps, Model, SoftDeletes


class Post(Model, HasTimestamps, SoftDeletes):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, nullable=False)
    name: Mapped[str] = mapped_column(String(64))
    content: Mapped[str] = mapped_column(Text)
