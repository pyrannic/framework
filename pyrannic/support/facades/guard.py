from pyrannic.contracts import AuthenticatableInterface, GuardInterface
from pyrannic.support.facades.facade import facade


@facade
class Guard(GuardInterface[AuthenticatableInterface]):
    """Facade for the guard interface."""

    @property
    def facade_accessor(self) -> str | type:
        return GuardInterface
