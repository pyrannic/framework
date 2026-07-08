from pyrannic.contracts.application import ApplicationInterface
from pyrannic.support.facades import facade


@facade("app")  # pyright: ignore[reportUntypedClassDecorator]
class CustomFacade(ApplicationInterface):
    """
    Custom facade for testing purposes.
    It passes the facade accessor to the `@facade` decorator.
    """
