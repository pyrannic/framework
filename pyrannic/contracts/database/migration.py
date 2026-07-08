from abc import ABC, abstractmethod

from .schema import SchemaInterface


class MigrationInterface(ABC):
    @abstractmethod
    async def up(self) -> None:
        """Defines the logic to apply the migration. This method should contain the code to create or modify database tables, columns, indexes, etc."""

    @abstractmethod
    async def down(self) -> None:
        """Defines the logic to revert the migration. This method should undo the changes made in the `up` method."""

    def set_schema(self, schema: SchemaInterface) -> None:
        """
        Sets the database schema for the migration.
        """
