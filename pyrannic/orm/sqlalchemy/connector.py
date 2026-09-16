import asyncio
from abc import ABC, abstractmethod
from collections.abc import AsyncGenerator
from logging import Logger
from os import path
from typing import Any, TypeVar

from sqlalchemy import Engine, create_engine
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import Session, sessionmaker

from pyrannic.contracts import (
    ApplicationInterface,
    ConfigRepositoryInterface,
    ConnectionDriverInterface,
    ConnectorInterface,
    MigrationInterface,
)
from pyrannic.ioc import Resolves
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
    _connection_driver: ConnectionDriverInterface

    def __init__(
        self,
        application: Resolves[ApplicationInterface],
        logger: Resolves[Logger],
        config: Resolves[ConfigRepositoryInterface],
        connection_driver: Resolves[ConnectionDriverInterface],
    ):
        self._application = application
        self._logger = logger
        self._config = config
        self._connection_driver = connection_driver

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

        if self._config.boolean("orm.drivers.sqlalchemy.alembic"):
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
    def url(self) -> str:
        """
        Returns the database URL from the configuration.
        """
        return self._connection_driver.url

    @property
    def alembic_config(self):
        from alembic.config import Config

        alembic_cfg = Config()
        alembic_cfg.set_main_option(
            "script_location",
            path.join("%(here)s", self._application.base_path, "database/migrations"),
        )

        alembic_cfg.set_main_option("sqlalchemy.url", self.url)
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

        return self._session

    async def disconnect(self) -> None:
        self._connection_driver.disconnect()
        self.engine.dispose()

    @property
    def engine(self) -> Engine:
        """
        Returns the SQLAlchemy engine instance.
        """

        if not self._engine:
            kwargs: dict[str, Any] = {
                "poolclass": self._config.get("orm.drivers.sqlalchemy.poolclass"),
                "pool_size": self._config.optional_integer(
                    "orm.drivers.sqlalchemy.pool_size"
                ),
                "max_overflow": self._config.optional_integer(
                    "orm.drivers.sqlalchemy.max_overflow"
                ),
                "creator": self._connection_driver.factory,
            }

            self._engine = create_engine(
                self.url,
                echo=self._config.boolean("orm.drivers.sqlalchemy.echo"),
                pool_recycle=self._config.integer(
                    "orm.drivers.sqlalchemy.pool_recycle"
                ),
                pool_pre_ping=self._config.boolean(
                    "orm.drivers.sqlalchemy.pool_pre_ping"
                ),
                future=self._config.boolean("orm.drivers.sqlalchemy.future"),
                **{k: v for k, v in kwargs.items() if v is not None},
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

        return self._session

    async def disconnect(self) -> None:
        result = self._connection_driver.disconnect()

        if result is not None:
            await result

        await self.engine.dispose()

    @property
    def engine(self) -> AsyncEngine:
        """
        Returns the SQLAlchemy async engine instance.
        """

        if not self._engine:
            kwargs: dict[str, Any] = {
                "poolclass": self._config.get("orm.drivers.sqlalchemy.poolclass"),
                "pool_size": self._config.optional_integer(
                    "orm.drivers.sqlalchemy.pool_size"
                ),
                "max_overflow": self._config.optional_integer(
                    "orm.drivers.sqlalchemy.max_overflow"
                ),
            }

            self._engine = create_async_engine(
                self.url,
                async_creator=self._connection_driver.factory,
                echo=self._config.boolean("orm.drivers.sqlalchemy.echo"),
                pool_recycle=self._config.integer(
                    "orm.drivers.sqlalchemy.pool_recycle"
                ),
                pool_pre_ping=self._config.boolean(
                    "orm.drivers.sqlalchemy.pool_pre_ping"
                ),
                future=self._config.boolean("orm.drivers.sqlalchemy.future"),
                **{k: v for k, v in kwargs.items() if v is not None},
            )

        return self._engine
