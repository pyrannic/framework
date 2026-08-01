from pyrannic.contracts.auth.auth_factory import AuthFactory
from pyrannic.contracts.auth.guard import GuardInterface
from pyrannic.ioc import Container


class AuthManager(AuthFactory):
    _guards: dict[str, GuardInterface] = {}
    """The dict of created "drivers"."""

    def __init__(self, container: Container) -> None:
        self._container = container

    def guard(self, name: str) -> GuardInterface:
        return super().guard(name)
