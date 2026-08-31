from pyrannic.contracts import AuthenticatableInterface, GuardInterface


class MyAwesomeGuard(GuardInterface[AuthenticatableInterface]):
    """
    A custom guard that implements the Guard Interface.
    """
