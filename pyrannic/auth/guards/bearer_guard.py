from typing import Annotated, Any

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from pyrannic.contracts import UserProviderInterface
from pyrannic.ioc import Resolves, scoped

from .base_guard import BaseGuard


@scoped
class BearerGuard(BaseGuard):
    model: HTTPAuthorizationCredentials

    def __init__(self, user_provider: Resolves[UserProviderInterface]):
        self.set_provider(user_provider)

    async def __ioc_call__(
        self,
        credentials: Annotated[
            HTTPAuthorizationCredentials | None,
            Depends(HTTPBearer()),
        ],
    ) -> None:
        if credentials and credentials.credentials:
            self.model = credentials
            await self.authenticate(credentials.credentials)

    async def authenticate(self, token: str) -> None:
        if token and self.validate(token):
            user = await self.provider.retrieve_by_credentials(token)

            if user and self.provider.validate_credentials(user, token):
                self.set_user(user)

    def validate(self, token: str, *args: Any, **kwargs: Any) -> bool:
        return True
