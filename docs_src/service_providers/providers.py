from typing import Type

from app.providers.app import AppServiceProvider

from pyrannic import (
    DatabaseServiceProvider,
    MiddlewaresServiceProvider,
    RoutersServiceProvider,
    ExceptionHandlersServiceProvider,
    ServiceProvider,
)

providers: list[Type[ServiceProvider]] = [
    ExceptionHandlersServiceProvider,
    AppServiceProvider,
    DatabaseServiceProvider,
    RoutersServiceProvider,
    MiddlewaresServiceProvider,
]
