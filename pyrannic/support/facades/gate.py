from pyrannic.contracts import GateInterface
from pyrannic.support.facades.facade import facade


@facade
class Gate(GateInterface):
    """Facade for the gate interface."""

    @property
    def facade_accessor(self) -> str | type:
        return GateInterface
