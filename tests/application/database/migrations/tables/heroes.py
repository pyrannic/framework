from pyrannic import Migration
from tests.application.app.models.hero import Hero


class HeroesTable(Migration):
    """
    Migration to create the 'heroes' table.
    """

    async def up(self) -> None:
        """
        Apply the migration: create the 'heroes' table.
        """
        await self.schema.create(Hero)

    async def down(self) -> None:
        """
        Revert the migration: drop the 'heroes' table.
        """
        await self.schema.drop(Hero)
