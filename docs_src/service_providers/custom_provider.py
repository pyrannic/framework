from typing import Type

from app.providers.app import AppServiceProvider
from app.providers.my_custom_provider import MyCustomServiceProvider

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
    MyCustomServiceProvider,
]

__all__ = ["providers"]
