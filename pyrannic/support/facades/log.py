from pyrannic import facade
from pyrannic.contracts import LoggerInterface


@facade
class Log(LoggerInterface):
    """Facade for the logging interface."""
