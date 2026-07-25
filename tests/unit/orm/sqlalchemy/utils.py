from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from pyrannic.database.migration import Migration
from pyrannic.orm.sqlalchemy.model import Model


class BarModel(Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255))


class BarsTable(Migration):
    async def up(self) -> None:
        await self.schema.create(BarModel)

    async def down(self) -> None:
        await self.schema.drop(BarModel)
