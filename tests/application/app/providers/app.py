from tests.application.app.services.foo import (
    BarService,
    FooService,
    FooService2,
    FooServiceInterface,
)

from pyrannic import ServiceProvider


class AppServiceProvider(ServiceProvider):
    __bindings__ = {
        FooServiceInterface: FooService,
    }

    def register(self):
        self.container.when(BarService).needs(FooServiceInterface).give(FooService2)
