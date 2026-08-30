import asyncio
from abc import ABC, abstractmethod
from collections.abc import AsyncGenerator
from logging import Logger
from os import path
from typing import Annotated, Any, TypeVar

from sqlalchemy import URL, Engine, create_engine
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_scoped_session,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import Session, scoped_session, sessionmaker

from pyrannic.container.params import Resolves
from pyrannic.contracts.application import ApplicationInterface
from pyrannic.contracts.config.repository import ConfigRepositoryInterface
from pyrannic.contracts.database.connector import ConnectorInterface
from pyrannic.contracts.database.migration import MigrationInterface
from pyrannic.orm.sqlalchemy.schema import Schema

EngineType = TypeVar("EngineType", bound=Engine | AsyncEngine)
SessionType = TypeVar(
    "SessionType",
    bound=sessionmaker[Session] | async_sessionmaker[AsyncSession],
)


class AbstractConnector[
    EngineType: Engine | AsyncEngine,
    SessionType: sessionmaker[Session] | async_sessionmaker[AsyncSession],
](ConnectorInterface, ABC):
    """
    Handles interactions with an SQL Database using SQLAlchemy.
    """

    _application: ApplicationInterface
    _logger: Logger
    _config: ConfigRepositoryInterface
    _engine: EngineType | None
    _session: SessionType | None

    def __init__(
        self,
        application: Annotated[ApplicationInterface, Resolves()],
        logger: Annotated[Logger, Resolves()],
        config: Annotated[ConfigRepositoryInterface, Resolves()],
    ):
        self._application = application
        self._logger = logger
        self._config = config

        if not hasattr(self, "_url"):
            self._url = None

        if not hasattr(self, "_engine"):
            self._engine = None

        if not hasattr(self, "_session"):
            self._session = None

    @property
    @abstractmethod
    def engine(self) -> EngineType:
        """
        Returns the SQLAlchemy engine instance.
        """

    async def migrate(
        self,
        migrations: list[type[MigrationInterface]] | None = None,
    ) -> None:
        async for migration in self._run_migrations(migrations):
            await migration.up()
            self._logger.info(f"|- ✅ Applied migration {migration.__class__.__name__}")

        if self._config.boolean("database.migrations.alembic"):
            await self._run_alembic_migrations()

    async def rollback(
        self,
        migrations: list[type[MigrationInterface]] | None = None,
    ) -> None:
        async for migration in self._run_migrations(migrations):
            await migration.down()
            self._logger.info(
                f"|- ✅ Rolled back migration {migration.__class__.__name__}"
            )

    @property
    def url(self) -> URL | str:
        """
        Returns the database URL from the configuration.
        """
        if not self._url:
            connection = self._config.string("database.connection", default="sqlite")
            url = self._config.optional_str(f"database.connections.{connection}.url")

            if url:
                self._url = url
            else:
                self._url = URL.create(
                    drivername=self._config.string(
                        f"database.connections.{connection}.driver"
                    ),
                    username=self._config.optional_str(
                        f"database.connections.{connection}.username"
                    ),
                    password=self._config.optional_str(
                        f"database.connections.{connection}.password"
                    ),
                    host=self._config.optional_str(
                        f"database.connections.{connection}.host"
                    ),
                    port=self._config.optional_int(
                        f"database.connections.{connection}.port"
                    ),
                    database=self._config.optional_str(
                        f"database.connections.{connection}.database"
                    ),
                )

        return self._url

    @property
    def alembic_config(self):
        from alembic.config import Config

        alembic_cfg = Config()
        alembic_cfg.set_main_option(
            "script_location",
            path.join("%(here)s", self._application.base_path, "database/migrations"),
        )
        alembic_cfg.set_main_option(
            "sqlalchemy.url",
            self.url
            if isinstance(self.url, str)
            else self.url.render_as_string(hide_password=False),
        )

        alembic_cfg.set_main_option(
            "pyrannic.asyncio",
            str(self._config.boolean("orm.drivers.sqlalchemy.asyncio")),
        )

        return alembic_cfg

    async def _run_migrations(
        self,
        migrations: list[type[MigrationInterface]] | None = None,
    ) -> AsyncGenerator[MigrationInterface, Any]:
        if migrations is not None:
            schema = Schema(self.engine, self._logger)

            for migration_cls in migrations:
                migration = migration_cls()
                migration.set_schema(schema)
                yield migration

    async def _run_alembic_migrations(self):
        """
        Run Alembic migrations using the configured database URL.
        """
        from alembic import command

        await asyncio.to_thread(command.upgrade, self.alembic_config, "head")
        self._logger.info("|- ✅ Applied Alembic migrations")


class Connector(AbstractConnector[Engine, sessionmaker[Session]]):
    """
    Handles synchronous interactions with an SQL Database using SQLAlchemy.
    """

    @property
    def connection(self) -> Any:
        if not self._session:
            self._session = sessionmaker(
                bind=self.engine,
                class_=Session,
                expire_on_commit=False,
            )

        return scoped_session(self._session)

    async def disconnect(self) -> None:
        self.engine.dispose()

    @property
    def engine(self) -> Engine:
        """
        Returns the SQLAlchemy engine instance.
        """

        # TODO: Use config.orm.sqlalchemy settings for pool size, echo, max_overflow, etc.

        if not self._engine:
            self._engine = create_engine(
                self.url,
                echo=False,
                # TODO pool_size=5,
                # TODO max_overflow=5,
                pool_pre_ping=True,
                future=True,  # lazy connections
            )

        return self._engine


class AsyncConnector(AbstractConnector[AsyncEngine, async_sessionmaker[AsyncSession]]):
    """
    Handles asynchronous interactions with an SQL Database using SQLAlchemy.
    """

    @property
    def connection(self) -> Any:
        if not self._session:
            self._session = async_sessionmaker(
                bind=self.engine,
                class_=AsyncSession,
                expire_on_commit=False,
            )

        return async_scoped_session(self._session, scopefunc=asyncio.current_task)

    async def disconnect(self) -> None:
        await self.engine.dispose()

    @property
    def engine(self) -> AsyncEngine:
        """
        Returns the SQLAlchemy async engine instance.
        """

        # TODO: Use config.orm.sqlalchemy settings for pool size, echo, etc.

        if not self._engine:
            self._engine = create_async_engine(
                self.url,
                echo=False,
                # TODO pool_size=5,
                # TODO max_overflow=5,
                pool_pre_ping=True,
                future=True,  # lazy connections
            )

        return self._engine
