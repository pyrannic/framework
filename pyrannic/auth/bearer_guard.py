from typing import Annotated

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from pyrannic.contracts import UserProviderInterface
from pyrannic.ioc import Resolves

from .base_guard import BaseGuard


class BearerGuard(BaseGuard):
    def __init__(self, user_provider: Resolves[UserProviderInterface]):
        self.set_provider(user_provider)

    async def __ioc_call__(
        self,
        credentials: Annotated[
            HTTPAuthorizationCredentials | None,
            Depends(HTTPBearer(auto_error=False), use_cache=False),
        ],
    ) -> None:
        token = credentials.credentials if credentials else None

        if token:
            user = await self.provider.retrieve_by_credentials(token=token)

            if user:
                self.set_user(user)
