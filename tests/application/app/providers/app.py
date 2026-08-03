from pyrannic import ServiceProvider
from pyrannic.contracts import GateInterface, UserProviderInterface
from pyrannic.ioc import Resolves
from tests.application.app.auth.user_provider import SQLAlchemyUserProvider
from tests.application.app.services.foo import (
    BarService,
    FooService,
    FooService2,
    FooServiceInterface,
)


class AppServiceProvider(ServiceProvider):
    __bindings__ = {
        FooServiceInterface: FooService,
    }

    def register(self):
        self.container.scoped(UserProviderInterface, SQLAlchemyUserProvider)
        self.container.when(BarService).needs(FooServiceInterface).give(FooService2)

    async def boot(self, gate: Resolves[GateInterface]) -> None:
        gate.define_ability("view_heroes", lambda user: True)  # type: ignore
        # gate.policy(Hero, HeroPolicy)
