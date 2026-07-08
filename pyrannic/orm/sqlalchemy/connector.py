import asyncio
from abc import ABC, abstractmethod
from logging import Logger
from typing import Annotated, Any, Generic, TypeVar

from sqlalchemy import URL, Engine, create_engine
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import Session, sessionmaker

from pyrannic.container.params import Resolves
from pyrannic.contracts.config.respository import ConfigRepositoryInterface
from pyrannic.contracts.database.connector import ConnectorInterface
from pyrannic.contracts.database.migration import MigrationInterface
from pyrannic.orm.sqlalchemy.schema import Schema

EngineType = TypeVar("EngineType", bound=Engine | AsyncEngine)
SessionType = TypeVar(
    "SessionType",
    bound=sessionmaker[Session] | async_sessionmaker[AsyncSession],
)


class AbstractSqlAlchemyConnector(
    ConnectorInterface, ABC, Generic[EngineType, SessionType]
):
    """
    Handles interactions with an SQL Database using SQLAlchemy.
    """

    _logger: Logger
    _config: ConfigRepositoryInterface
    _engine: EngineType | None
    _session: SessionType | None

    def __init__(
        self,
        logger: Annotated[Logger, Resolves()],
        config: Annotated[ConfigRepositoryInterface, Resolves()],
    ):
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
        pass

    async def migrate(
        self,
        migrations: list[type[MigrationInterface]] | None = None,
    ) -> None:
        await self._run_migrations(migrations)

        if self._config.boolean("database.migrations.alembic"):
            await self._run_alembic_migrations()

    @property
    def url(self) -> URL:
        """
        Returns the database URL from the configuration.
        """
        if not self._url:
            connection = self._config.string("database.connection", default="sqlite")

            self._url = URL.create(
                drivername=self._config.string(
                    f"database.connections.{connection}.driver"
                ),
                username=self._config.string(
                    f"database.connections.{connection}.username"
                ),
                password=self._config.string(
                    f"database.connections.{connection}.password"
                ),
                host=self._config.string(f"database.connections.{connection}.host"),
                port=self._config.integer(f"database.connections.{connection}.port"),
                database=self._config.string(
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
            "%(here)s/database/migrations",
        )
        alembic_cfg.set_main_option(
            "sqlalchemy.url", self.url.render_as_string(hide_password=False)
        )

        alembic_cfg.set_main_option(
            "pyranninc.asyncio",
            str(self._config.boolean("services.sqlalchemy.asyncio")),
        )

        return alembic_cfg

    async def _run_migrations(
        self, migrations: list[type[MigrationInterface]] | None = None
    ) -> None:
        if migrations is not None:
            schema = Schema(self.engine, self._logger)

            for migration_cls in migrations:
                migration = migration_cls()
                migration.set_schema(schema)
                await migration.up()
                self._logger.info(f"|- ✅ Applied migration {migration_cls.__name__}")

    async def _run_alembic_migrations(self):
        """
        Run Alembic migrations using the configured database URL.
        """
        from alembic import command

        await asyncio.to_thread(command.upgrade, self.alembic_config, "head")
        self._logger.info("|- ✅ Applied Alembic migrations")


class SqlAlchemyConnector(AbstractSqlAlchemyConnector[Engine, sessionmaker[Session]]):
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
        self.engine.dispose()

    @property
    def engine(self) -> Engine:
        """
        Returns the SQLAlchemy engine instance.
        """

        # TODO: Use config.services.sqlalchemy settings for pool size, echo, etc.

        if not self._engine:
            self._engine = create_engine(
                self.url,
                echo=False,
                pool_size=5,
                max_overflow=5,
                pool_pre_ping=True,
                future=True,  # lazy connections
            )

        return self._engine


class SqlAlchemyAsyncConnector(
    AbstractSqlAlchemyConnector[AsyncEngine, async_sessionmaker[AsyncSession]]
):
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
        await self.engine.dispose()

    @property
    def engine(self) -> AsyncEngine:
        """
        Returns the SQLAlchemy async engine instance.
        """

        # TODO: Use config.services.sqlalchemy settings for pool size, echo, etc.

        if not self._engine:
            self._engine = create_async_engine(
                self.url,
                echo=False,
                pool_size=5,
                max_overflow=5,
                pool_pre_ping=True,
                future=True,  # lazy connections
            )

        return self._engine
