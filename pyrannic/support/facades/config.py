from pyrannic.contracts.config.respository import ConfigRepositoryInterface
from pyrannic.support.facades.facade import facade


@facade
class Config(ConfigRepositoryInterface):
    """Facade for the configuration repository interface."""
