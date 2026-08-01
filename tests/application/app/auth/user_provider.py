from typing import Any

from pyrannic.contracts import (
    AuthenticatableInterface,
    UserProviderInterface,
)
from pyrannic.ioc import Resolves
from tests.application.app.repositories.users import UsersRepository


class SQLAlchemyUserProvider(UserProviderInterface):
    def __init__(self, repository: Resolves[UsersRepository]):
        self._repository = repository

    async def retrieve_by_id(self, identifier: str) -> AuthenticatableInterface | None:
        return self._repository.find(identifier)

    async def retrieve_by_credentials(
        self,
        token: str,
    ) -> AuthenticatableInterface | None:
        return self._repository.first()  # TODO

    def validate_credentials(
        self,
        user: AuthenticatableInterface,
        credentials: dict[str, Any],
    ) -> bool:
        return False
