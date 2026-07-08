from typing import Annotated

from pyrannic import Resolves, ServiceProvider
from pyrannic.contracts import DatabaseManagerInterface

from app.database.manager import DatabaseManager


class DatabaseServiceProvider(ServiceProvider):
    __singletons__ = {
        DatabaseManagerInterface: DatabaseManager,
    }
