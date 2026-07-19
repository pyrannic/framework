from tests.application.app.providers.app import AppServiceProvider

from pyrannic import (
    DatabaseServiceProvider,
    MiddlewaresServiceProvider,
    RoutersServiceProvider,
    ExceptionHandlersServiceProvider,
    ServiceProvider,
)

providers: list[type[ServiceProvider]] = [
    ExceptionHandlersServiceProvider,
    AppServiceProvider,
    DatabaseServiceProvider,
    RoutersServiceProvider,
    MiddlewaresServiceProvider,
]

__all__ = ["providers"]
