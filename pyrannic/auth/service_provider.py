from pyrannic.auth.access.gate import Gate
from pyrannic.auth.guards.bearer_guard import BearerGuard
from pyrannic.auth.guards.jwt_guard import JwtGuard
from pyrannic.auth.safeguard import Safeguard
from pyrannic.bootstrap.service_provider import ServiceProvider
from pyrannic.contracts import (
    AuthenticatableInterface,
    ConfigRepositoryInterface,
    GateInterface,
    GuardInterface,
)
from pyrannic.ioc import Resolves


class AuthServiceProvider(ServiceProvider):
    def register(self) -> None:
        self.config = self.container.instance(ConfigRepositoryInterface)

        self.container.bind_if(GuardInterface, self.guard_concrete_type)
        self.container.bind_if(GateInterface, Gate)

        self.register_security_model()

    async def boot(
        self,
        gate: Resolves[GateInterface],
        guard: Resolves[GuardInterface[AuthenticatableInterface]],
    ) -> None:
        # Register the Gate & Guard instances to be used in their Facades.
        self.container.instance(GateInterface, gate)
        self.container.instance(GuardInterface, guard)

    def register_security_model(self) -> None:
        model = self.config.get(f"auth.guards.{self.guard_driver}.security_model")

        if model:
            Safeguard.use_security_model(model)

    @property
    def guard_driver(self) -> str:
        return self.config.str("auth.guard", "bearer")

    @property
    def guard_concrete_type(self) -> type[GuardInterface[AuthenticatableInterface]]:
        if self.guard_driver == "jwt":
            return JwtGuard

        return BearerGuard
