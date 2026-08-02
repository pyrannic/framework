from pyrannic.auth.access.gate import Gate
from pyrannic.auth.bearer_guard import BearerGuard
from pyrannic.auth.safeguard import Safeguard
from pyrannic.bootstrap.service_provider import ServiceProvider
from pyrannic.contracts import (
    AuthenticatableInterface,
    ConfigRepositoryInterface,
    GateInterface,
    GuardInterface,
)


class AuthServiceProvider(ServiceProvider):
    __bindings__ = {
        GuardInterface[AuthenticatableInterface]: BearerGuard,
        GateInterface: Gate,
    }

    def register(self) -> None:
        self._register_security_model()

    def _register_security_model(self) -> None:
        config = self.container.instance(ConfigRepositoryInterface)
        guard_name = config.get("auth.guard", "bearer")
        model = config.get(f"auth.guards.{guard_name}.security_model")

        if model:
            Safeguard.use_security_model(model)
