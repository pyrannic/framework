from contextlib import asynccontextmanager
from logging import Logger
import os
from typing import AsyncGenerator, Self, Type

from dotenv import load_dotenv

from pyrannic.bootstrap.service_provider import ServiceProvider
from pyrannic.contracts.application import ApplicationInterface
from pyrannic.support.facades.facade import Facade
from pyrannic.support.reflection import get_attr


class BootstrapManager:
    _service_provider_classes: list[Type[ServiceProvider]]
    _service_provider_instances: list[ServiceProvider]
    _running = False
    _critical_services_started = False

    def __init__(
        self,
        service_providers: list[Type[ServiceProvider]] | None = None,
    ) -> None:
        self._service_provider_classes = service_providers or []
        self._service_provider_instances = []

    def start_critical_services(
        self,
        app: ApplicationInterface,
        services: list[type[ServiceProvider]],
    ) -> Self:
        """
        Configure critical services like config, logging, etc. that may be needed during the bootstrapping process.

        After calling this method:
            - The BootstrapManager is ready to run the bootstrapping process.
            - The Facade is configured with the application instance.
            - The critical services are registered and available for use.
            - The environment variables from the .env file are loaded into the application.
        """
        load_dotenv(os.path.join(app.base_path, ".env"))
        Facade.set_facade_application(app)

        for provider_class in services:
            provider_class(app).register()

        self._logger = app.container.instance(Logger)
        self._critical_services_started = True

        return self

    def run(self, app: ApplicationInterface) -> Self:
        """Registers service providers and starts the bootstrapping process."""

        if not self._critical_services_started:
            raise RuntimeError(
                "Critical services must be started before running the bootstrap manager"
            )

        self._service_provider_classes = self._discover_service_providers(app)
        self._running = True
        self._logger.info("🕒 Initializing application...")

        for ProviderClass in self._service_provider_classes:
            provider = ProviderClass(app, self._logger)
            name = ProviderClass.__name__

            try:
                self._register_provider(provider)
                self._service_provider_instances.append(provider)
                self._logger.info(f"✅ Registered {name}")
            except Exception as e:
                self._provider_exec_failed(provider, "register", e)

        return self

    @asynccontextmanager
    async def lifespan(self, app: ApplicationInterface) -> AsyncGenerator[None, None]:
        self._logger.info("↗️  Starting up application...")

        await self._walk_providers(app, "initialize", "Initialized")
        await self._walk_providers(app, "boot", "Booted")

        yield

        self._running = False
        self._logger.info("↘️  Shutting down application...")
        await self._walk_providers(app, "shutdown", "Shutdown", should_reverse=True)
        self._logger.info("✅ Resources released and application shutdown complete")

    async def _walk_providers(
        self,
        app: ApplicationInterface,
        method_name: str,
        info_message: str,
        should_reverse: bool = False,
    ) -> None:
        providers = (
            self._service_provider_instances[::-1]
            if should_reverse
            else self._service_provider_instances
        )

        for provider in providers:
            try:
                method = getattr(provider, method_name, None)

                if method is not None:
                    await app.container.call(method)
                    self._logger.info(
                        f"✅ {info_message} {provider.__class__.__name__}"
                    )
            except Exception as e:
                self._provider_exec_failed(provider, method_name, e)

    def _provider_exec_failed(
        self,
        provider: ServiceProvider,
        method_name: str,
        exception: Exception,
    ):
        name = provider.__class__.__name__

        if self._running and provider.is_critical:
            self._logger.critical(
                f"❌  {name} failed to {method_name}, cannot start app"
            )
            raise provider.exception(f"{name} failed to {method_name}") from exception
        else:
            self._logger.warning(
                f"⚠️  {name} failed to {method_name} properly: {exception}"
            )

            if self._running:
                provider.failed(method_name)

    def _register_provider(self, provider: ServiceProvider):
        for abstract, concrete in provider.__bindings__.items():
            provider.app.container.bind(abstract, concrete)

        for abstract, concrete in provider.__singletons__.items():
            provider.app.container.singleton(abstract, concrete)

        provider.register()

    def _discover_service_providers(
        self,
        app: ApplicationInterface,
    ) -> list[Type[ServiceProvider]]:
        if bool(self._service_provider_classes):
            return self._service_provider_classes

        return get_attr(
            os.path.join(app.base_path, "bootstrap/providers"),
            "providers",
            [],
        )
