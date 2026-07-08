from abc import ABC
from logging import Logger
from typing import Any

from pyrannic.contracts.application import ApplicationInterface
from pyrannic.contracts.container.container import ContainerInterface


class ServiceProvider(ABC):
    def __init__(self, app: ApplicationInterface, logger: Logger | None = None):
        self.app = app
        self.logger = logger

    __bindings__: dict[str | type, type] = {}
    """All of the container bindings that should be registered."""

    __singletons__: dict[str | type, type] = {}
    """All of the container singletons that should be registered."""

    @property
    def container(self) -> ContainerInterface:
        return self.app.container

    @property
    def is_critical(self) -> bool:
        """
        Indicates whether the service provider is critical for the application startup.
        If a critical service provider fails during initialization or boot, the application will not start.
        """
        return False

    def register(self):
        """
        Register services, routes, middlewares and other components.
        This method is called during the application startup phase, and it should be used to set up the necessary components for the application to function properly.
        It can't be async method, because it is called before the application is fully initialized, and it should not perform any asynchronous operations.
        """

    def initialize(self, *args: Any, **kwargs: Any) -> Any:
        """
        Initialize services and other components.
        This method is called after the application has been fully initialized, and it should be used to perform any necessary setup that requires the application to be fully functional.
        It can be async method, because it is called after the application is fully initialized, and it can perform asynchronous operations if needed.
        """

    def boot(self, *args: Any, **kwargs: Any) -> Any:
        """
        Boot services and other components.
        This method is called after the application has been fully initialized and all services have been registered and initialized, and it should be used to perform any necessary setup that requires all services to be fully functional.
        It can be async method, because it is called after the application is fully initialized, and it can perform asynchronous operations if needed.
        """

    def shutdown(self, *args: Any, **kwargs: Any) -> Any:
        """
        Shutdown services and other components.
        This method is called during the application shutdown phase, and it should be used to perform any necessary cleanup operations.
        It can be async method, because it is called during the application shutdown phase, and it can perform asynchronous operations if needed.
        """

    def failed(self, stage_name: str):
        """
        Handle failure of a non-critical service provider during initialization or boot.
        This method can be overridden by non-critical service providers to perform specific actions when they fail during initialization or boot, such as setting internal flags or performing cleanup operations.
        """

    def exception(self, message: str | None = None) -> Exception:
        """
        Return an exception to be raised when a critical service provider fails during initialization or boot.
        This method can be overridden by critical service providers to return a specific exception type with a custom message.
        """
        return Exception(message)
