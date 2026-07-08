from typing import Any

from pyrannic.bootstrap.manager import BootstrapManager
from pyrannic.bootstrap.service_provider import ServiceProvider
from pyrannic.config.provider import ConfigRepositoryProvider
from pyrannic.container.container import Container
from pyrannic.contracts.application import ApplicationInterface
from pyrannic.contracts.container.container import ContainerInterface
from pyrannic.http.middlewares.forget_scoped_instances import (
    ForgetScopedInstancesMiddleware,
)
from pyrannic.logging.provider import LoggingServiceProvider
from pyrannic.support.facades.config import Config


class Application(ApplicationInterface):
    _critical_service_providers: list[type[ServiceProvider]] = [
        ConfigRepositoryProvider,
        LoggingServiceProvider,
    ]

    def __init__(
        self,
        *,
        debug: bool = False,
        version: str = "0.1.0",
        title: str | None = None,
        base_path: str = "",
        **kwargs: Any,
    ) -> None:
        self._base_path = base_path
        bootstrap_manager = BootstrapManager()

        super().__init__(lifespan=bootstrap_manager.lifespan, **kwargs)

        bootstrap_manager.start_critical_services(
            self,
            self._critical_service_providers,
        )

        self.title = Config.string("app.name", title or "Pyrannic Application")
        self.debug = Config.boolean("app.debug", debug)
        self.version = Config.string("app.version", version)

        bootstrap_manager.run(self)
        self.add_middleware(ForgetScopedInstancesMiddleware)

    @property
    def base_path(self) -> str:
        return self._base_path

    @property
    def container(self) -> ContainerInterface:
        if not hasattr(self, "_container"):
            self._container = Container(self)
            self._container.instance(ApplicationInterface, self)
            self._container.instance(ContainerInterface, self._container)
            self._container.set_alias(ApplicationInterface, "app")

        return self._container
