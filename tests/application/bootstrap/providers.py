from pyrannic import (
    ExceptionHandlersServiceProvider,
    MiddlewaresServiceProvider,
    RoutersServiceProvider,
    ServiceProvider,
)
from pyrannic.orm.sqlalchemy import DatabaseServiceProvider
from tests.application.app.providers.app import AppServiceProvider

providers: list[type[ServiceProvider]] = [
    ExceptionHandlersServiceProvider,
    AppServiceProvider,
    DatabaseServiceProvider,
    RoutersServiceProvider,
    MiddlewaresServiceProvider,
]

__all__ = ["providers"]
