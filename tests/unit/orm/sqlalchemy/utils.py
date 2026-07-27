from logging import Logger
from typing import Annotated
from unittest.mock import Mock

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column, relationship

import pyrannic.support.string as string
from pyrannic.container.param_functions import Resolves
from pyrannic.contracts import ApplicationInterface, DatabaseManagerInterface
from pyrannic.database.migration import Migration
from pyrannic.orm.sqlalchemy import (
    DatabaseServiceProvider,
    HasTimestamp,
    HasTimestamps,
    Model,
    SoftDeletes,
)


class MockDatabaseServiceProvider(DatabaseServiceProvider):
    def __init__(self, app: ApplicationInterface, logger: Logger | None = None):
        super().__init__(app, logger)
        self.mock = Mock(spec=self)
        self.mock.container = self.container

    @property
    def is_critical(self) -> bool:
        self.mock.is_critical()
        return not super().is_critical

    def register(self) -> None:
        self.mock.register()
        self.container.instance(self.__class__.__name__, self.mock)
        super().register()

    async def initialize(self) -> None:
        await self.mock.initialize()
        await super().initialize()

    async def boot(
        self, manager: Annotated[DatabaseManagerInterface, Resolves()]
    ) -> None:
        await self.mock.boot(manager)
        await super().boot(manager)

    async def shutdown(
        self, manager: Annotated[DatabaseManagerInterface, Resolves()]
    ) -> None:
        await self.mock.shutdown(manager)
        await super().shutdown(manager)


class BarModel(Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255))
    parent_id: Mapped[int] = mapped_column(ForeignKey("bars.id"), nullable=True)
    parent: Mapped["BarModel | None"] = relationship(
        remote_side=[id],
        back_populates="children",
    )
    children: Mapped[list["BarModel"]] = relationship(back_populates="parent")

    @hybrid_property
    def slug(self) -> str:
        return string.to_kebab_case(self.name)

    @property
    def upper_name(self) -> str:
        return self.name.upper()


class HasTimestampModel(Model, HasTimestamp):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)


class HasTimestampsModel(Model, HasTimestamps):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)


class SoftDeletesModel(Model, SoftDeletes):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)


class BarsTable(Migration):
    async def up(self) -> None:
        await self.schema.create(BarModel)

    async def down(self) -> None:
        await self.schema.drop(BarModel)
