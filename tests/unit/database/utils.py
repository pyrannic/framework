from pyrannic.database.migration import Migration


class FooTable(Migration):
    async def up(self) -> None:
        await self.schema.create("foo_table")

    async def down(self) -> None:
        await self.schema.drop("foo_table")
