from pyrannic.contracts.application import ApplicationInterface
from pyrannic.support.facades.facade import facade


@facade
class App(ApplicationInterface):
    """Facade for the Pyrannic application interface."""
