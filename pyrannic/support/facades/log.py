from pyrannic.contracts import LoggerInterface
from pyrannic.support.facades.facade import facade


@facade
class Log(LoggerInterface):
    """Facade for the logging interface."""
