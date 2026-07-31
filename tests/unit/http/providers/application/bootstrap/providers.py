from pyrannic import ServiceProvider
from pyrannic.orm.sqlalchemy.provider import DatabaseServiceProvider
from tests.application.app.providers.app import AppServiceProvider

providers: list[type[ServiceProvider]] = [
    AppServiceProvider,
    DatabaseServiceProvider,
]

__all__ = ["providers"]
