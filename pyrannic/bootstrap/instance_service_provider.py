from abc import abstractmethod
import inspect
from typing import Any, Generic, TypeVar

from pyrannic.bootstrap.service_provider import ServiceProvider
from pyrannic.support.reflection import get_generic_type

ServiceType = TypeVar("ServiceType")


class InstanceServiceProvider(ServiceProvider, Generic[ServiceType]):
    @property
    def _has_dependencies(self) -> bool:
        argspec = inspect.getfullargspec(self._create)
        return len(argspec.args) > 1

    @property
    def abstract(self) -> str | type:
        return get_generic_type(self)

    @property
    def aliases(self) -> list[str | type] | None:
        return None

    @abstractmethod
    def _create(self, *args: Any, **kwargs: Any) -> ServiceType:
        """
        Create an instance of the service.
        This method should be implemented by subclasses to provide the logic for creating the service instance.
        It can be asynchronous and also it can accept injected dependencies as parameters if needed.
        """

    def register(self):
        if not self._has_dependencies:
            self._set_instance(self._create())

    async def boot(self):
        if self._has_dependencies:
            self._set_instance(await self.app.container.call(self._create))

    def _set_instance(self, instance: ServiceType):
        abstract = self.abstract
        aliases = self.aliases

        self.app.container.instance(abstract, instance)

        if bool(aliases):
            for alias in aliases:
                self.app.container.set_alias(abstract, alias)
