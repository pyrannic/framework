from pyrannic import Migration
from tests.application.app.models.user import User


class UsersTable(Migration):
    async def up(self) -> None:
        await self.schema.create(User)

    async def down(self) -> None:
        await self.schema.drop(User)
