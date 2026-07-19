from typing import Annotated
from pyrannic import Resolves
from pyrannic.contracts import ConfigRepositoryInterface


def resolver(config_repository: Annotated[ConfigRepositoryInterface, Resolves()]):
    unused_value = config_repository.get("app.debug")
