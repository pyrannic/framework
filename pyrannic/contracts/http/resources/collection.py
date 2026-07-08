from typing import TypeVar

from pyrannic.contracts.http.resources.resource import ResourceInterface

DataType = TypeVar("DataType", covariant=True, bound=ResourceInterface)


class ResourceCollectionInterface:
    pass
