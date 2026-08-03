from pyrannic.auth.access.gate import GateInterface
from pyrannic.auth.safeguard import Safeguard
from pyrannic.auth.service_provider import AuthServiceProvider
from pyrannic.contracts.application import ApplicationInterface
from pyrannic.contracts.auth import AuthenticatableInterface
from pyrannic.contracts.auth.guard import GuardInterface


def test_service_provider(application: ApplicationInterface):
    provider = AuthServiceProvider(application)
    provider.register()

    assert application.container.is_bound(GuardInterface[AuthenticatableInterface])
    assert application.container.is_bound(GateInterface)
    assert Safeguard.get_security_model() is not None
