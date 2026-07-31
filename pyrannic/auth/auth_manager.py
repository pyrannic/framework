from pyrannic.contracts.auth.auth_factory import AuthFactory
from pyrannic.contracts.auth.guard import GuardInterface


class AuthManager(AuthFactory):
    _guards: dict[str, GuardInterface] = {}
    """The dict of created "drivers"."""

    def guard(self, name: str) -> GuardInterface:
        return super().guard(name)
