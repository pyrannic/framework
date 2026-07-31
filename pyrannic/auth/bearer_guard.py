from typing import Annotated

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from pyrannic.contracts import UserProviderInterface
from pyrannic.ioc import Resolves

from .base_guard import BaseGuard


class BearerGuard(BaseGuard):
    def __init__(
        self,
        user_provider: Resolves[UserProviderInterface],
        credentials: Annotated[HTTPAuthorizationCredentials, Depends(HTTPBearer())],
    ):
        self._token = credentials.credentials
        self.set_provider(user_provider)

    async def __call__(self) -> None:
        # TODO await self.provider.retrieve_by_token(self.id, self._token)
        pass
