from typing import Annotated, TypeVar

from pyrannic.container import param_functions
from pyrannic.container.decorators import scoped as scoped
from pyrannic.container.decorators import singleton as singleton
from pyrannic.contracts.application import ApplicationInterface
from pyrannic.contracts.container.container import ContainerInterface

T = TypeVar("T")

Resolves = Annotated[T, param_functions.Resolves()]
Singleton = Annotated[T, param_functions.Singleton()]
Scoped = Annotated[T, param_functions.Scoped()]

Container = Resolves[ContainerInterface]
App = Resolves[ApplicationInterface]
