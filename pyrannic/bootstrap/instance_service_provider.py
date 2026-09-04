import inspect
from abc import abstractmethod
from typing import Any

from pyrannic.bootstrap.service_provider import ServiceProvider
from pyrannic.support.reflection import get_generic_type


class InstanceServiceProvider[ServiceType](ServiceProvider):
    @property
    def _has_dependencies(self) -> bool:
        argspec = inspect.getfullargspec(self._create)
        return len(argspec.args) > 1

    @property
    def abstract(self) -> str | type:
        abstract = get_generic_type(self)

        assert abstract is not None, (
            "The abstract type must be specified in the generic type of the InstanceServiceProvider."
        )

        return abstract

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
