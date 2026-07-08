from pyrannic.contracts.database.migration import MigrationInterface
from pyrannic.contracts.database.schema import SchemaInterface


class Migration(MigrationInterface):
    schema: SchemaInterface

    def set_schema(self, schema: SchemaInterface) -> None:
        self.schema = schema
