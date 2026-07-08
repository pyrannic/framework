from tests.application.app.providers.app import AppServiceProvider

from pyrannic import (
    DatabaseServiceProvider,
    ServiceProvider,
)

providers: list[type[ServiceProvider]] = [
    AppServiceProvider,
    DatabaseServiceProvider,
]
