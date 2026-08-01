from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from pyrannic.auth import Authenticatable, Authorizable
from pyrannic.orm.sqlalchemy import HasTimestamps, Model


class User(Model, HasTimestamps, Authenticatable, Authorizable):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(64))
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    password: Mapped[str] = mapped_column(String(255))
