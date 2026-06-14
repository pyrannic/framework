from pyrannic import ServiceProvider
from pyrannic.contracts import DatabaseManagerInterface

from app.database.manager import DatabaseManager


class DatabaseServiceProvider(ServiceProvider):
    def register(self):
        self.container.singleton(DatabaseManagerInterface, DatabaseManager)
