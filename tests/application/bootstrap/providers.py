from pyrannic import (
    ExceptionHandlersServiceProvider,
    MiddlewaresServiceProvider,
    RoutersServiceProvider,
    ServiceProvider,
)
from pyrannic.auth.service_provider import AuthServiceProvider
from pyrannic.orm.sqlalchemy import DatabaseServiceProvider
from tests.application.app.providers.app import AppServiceProvider

providers: list[type[ServiceProvider]] = [
    ExceptionHandlersServiceProvider,
    AppServiceProvider,
    DatabaseServiceProvider,
    RoutersServiceProvider,
    MiddlewaresServiceProvider,
    AuthServiceProvider,
]

__all__ = ["providers"]
