from logging import Logger
from unittest.mock import Mock

from pyrannic.bootstrap.instance_service_provider import (
    InstanceServiceProvider as BaseInstanceServiceProvider,
)
from pyrannic.ioc import Resolve


class InstanceServiceProvider(BaseInstanceServiceProvider[Mock]):
    @property
    def aliases(self) -> list[str | type]:
        return ["mock", "fake", "dummy"]

    def _create(self) -> Mock:
        return Mock()


class InstanceServiceProviderWithDependencies(BaseInstanceServiceProvider[Mock]):
    def _create(self, logger: Resolve[Logger]) -> Mock:
        mock = Mock()
        mock.create(logger)

        return mock
