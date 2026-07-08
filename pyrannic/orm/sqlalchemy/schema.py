from logging import Logger
from typing import Any, Callable

from sqlalchemy import Engine, FromClause
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.orm import DeclarativeBase

from pyrannic.contracts.database.schema import SchemaInterface


class Schema(SchemaInterface):
    _engine: AsyncEngine | Engine
    _logger: Logger

    def __init__(self, engine: AsyncEngine | Engine, logger: Logger):
        self._engine = engine
        self._logger = logger

    async def create(self, blueprint: DeclarativeBase) -> None:
        """
        Creates the conversation table in the database if it does not exist.
        """
        await self._run(
            blueprint.__table__,
            blueprint.__tablename__,
            blueprint.metadata.create_all,
            "Failed to create {} table: {}",
        )

    async def drop(self, blueprint: DeclarativeBase) -> None:
        """
        Drops the conversation table from the database if it exists.
        """
        await self._run(
            blueprint.__table__,
            blueprint.__tablename__,
            blueprint.metadata.drop_all,
            "Failed to drop {} table: {}",
        )

    async def _run(
        self,
        table: FromClause,
        table_name: str,
        callback: Callable[..., Any],
        exception_msg: str,
    ) -> None:
        try:
            if isinstance(self._engine, AsyncEngine):
                async with self._engine.begin() as conn:
                    await conn.run_sync(callback, tables=[table])
            else:
                callback(self._engine, tables=[table])
        except Exception as e:
            self._logger.error(exception_msg.format(table_name, str(e)))
