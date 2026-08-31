from app.auth.my_awesome_guard import MyAwesomeGuard

from pyrannic import ServiceProvider
from pyrannic.contracts import AuthenticatableInterface, GuardInterface


class AppServiceProvider(ServiceProvider):
    def register(self):
        self.container.scoped(GuardInterface[AuthenticatableInterface], MyAwesomeGuard)
