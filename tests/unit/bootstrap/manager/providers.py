from logging import Logger
from typing import Annotated, Any
from unittest.mock import Mock

from pyrannic.bootstrap.service_provider import ServiceProvider
from pyrannic.container.param_functions import Resolves
from pyrannic.contracts.application import ApplicationInterface
from pyrannic.contracts.config.respository import ConfigRepositoryInterface
from pyrannic.support.string import to_snake_case


class MockServiceProvider(ServiceProvider):
    @property
    def instance_key(self) -> str:
        return to_snake_case(self.__class__.__name__.removesuffix("Provider"))

    def __init__(self, app: ApplicationInterface, logger: Logger | None = None):
        super().__init__(app, logger)
        self.mock = Mock(spec=self)
        self.mock.container = self.container

    def register(self) -> None:
        self.mock.register()
        self.container.instance(self.instance_key, self.mock)

    async def initialize(
        self,
        config: Annotated[ConfigRepositoryInterface, Resolves("config")],
    ) -> None:
        await self.mock.initialize(config)

    async def boot(
        self,
        config: Annotated[ConfigRepositoryInterface, Resolves("config")],
    ) -> None:
        await self.mock.boot(config)

    def shutdown(self, *args: Any, **kwargs: Any) -> Any:
        self.mock.shutdown(*args, **kwargs)

    def failed(self, stage_name: str):
        self.mock.failed(stage_name)


class FooServiceProvider(MockServiceProvider):
    pass


class BarServiceProvider(MockServiceProvider):
    def register(self) -> None:
        super().register()
        raise RuntimeError("BarServiceProvider register method called")


class BazServiceProvider(MockServiceProvider):
    @property
    def is_critical(self) -> bool:
        return True

    def register(self) -> None:
        super().register()
        raise RuntimeError("BazServiceProvider register method called")


class UninitializableServiceProvider(MockServiceProvider):
    async def initialize(
        self,
        config: Annotated[ConfigRepositoryInterface, Resolves("config")],
    ) -> None:
        await super().initialize(config)
        raise RuntimeError("UninitializableServiceProvider initialize method called")


class UninitializableCriticalServiceProvider(MockServiceProvider):
    @property
    def is_critical(self) -> bool:
        return True

    async def initialize(
        self,
        config: Annotated[ConfigRepositoryInterface, Resolves("config")],
    ) -> None:
        await super().initialize(config)
        raise RuntimeError("UninitializableServiceProvider initialize method called")


class UnbootableServiceProvider(MockServiceProvider):
    async def boot(
        self,
        config: Annotated[ConfigRepositoryInterface, Resolves("config")],
    ) -> None:
        await super().boot(config)
        raise RuntimeError("UnbootableServiceProvider boot method called")


class UnbootableCriticalServiceProvider(MockServiceProvider):
    @property
    def is_critical(self) -> bool:
        return True

    async def boot(
        self,
        config: Annotated[ConfigRepositoryInterface, Resolves("config")],
    ) -> None:
        await super().boot(config)
        raise RuntimeError("UnbootableCriticalServiceProvider boot method called")


class ServiceProviderWithSingletons(MockServiceProvider):
    __singletons__: dict[str | type, type] = {
        "foo_singleton": Mock,
        "bar_singleton": Mock,
        "baz_singleton": Mock,
    }


class ServiceProviderWithBindings(MockServiceProvider):
    __bindings__: dict[str | type, type] = {
        "foo_service": Mock,
        "bar_service": Mock,
        "baz_service": Mock,
    }
