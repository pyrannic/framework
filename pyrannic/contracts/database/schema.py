from abc import ABC
from typing import Any


class SchemaInterface(ABC):
    async def create(self, blueprint: Any) -> None:
        """
        Creates the table in the database if it does not exist.
        """
        pass

    async def drop(self, blueprint: Any) -> None:
        """
        Drops the table from the database if it exists.
        """
        pass
