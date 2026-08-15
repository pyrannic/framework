import pytest

from pyrannic.auth.access.gate import GateInterface
from pyrannic.auth.guards.bearer_guard import BearerGuard
from pyrannic.auth.safeguard import Safeguard
from pyrannic.auth.service_provider import AuthServiceProvider
from pyrannic.contracts import ConfigRepositoryInterface
from pyrannic.contracts.application import ApplicationInterface
from pyrannic.contracts.auth import AuthenticatableInterface
from pyrannic.contracts.auth.guard import GuardInterface


def test_service_provider(application: ApplicationInterface):
    provider = AuthServiceProvider(application)
    provider.register()

    assert application.container.is_bound(GuardInterface[AuthenticatableInterface])
    assert application.container.is_bound(GateInterface)
    assert Safeguard.get_security_model() is not None


@pytest.mark.asyncio
async def test_guard_concrete_type(application: ApplicationInterface):
    config: ConfigRepositoryInterface = await application.container.resolve("config")
    config.set("auth.guard", "bearer")

    provider = AuthServiceProvider(application)
    provider.register()

    guard_concrete_type = provider.guard_concrete_type

    assert guard_concrete_type is not None
    assert issubclass(guard_concrete_type, BearerGuard)
