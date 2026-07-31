from typing import Any

from pyrannic.contracts import (
    AuthenticatableInterface,
    RepositoryInterface,
    UserProviderInterface,
)


class SQLAlchemyUserProvider(UserProviderInterface):
    def __init__(self, repository: RepositoryInterface[Any]):
        self._repository = repository

    async def retrieve_by_id(self, identifier: Any) -> AuthenticatableInterface | None:
        return None

    async def retrieve_by_token(
        self,
        identifier: Any,
        token: str,
    ) -> AuthenticatableInterface | None:
        return None

    async def update_remember_token(
        self,
        user: AuthenticatableInterface,
        token: str,
    ) -> None:
        pass
