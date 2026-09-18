from azure.identity import DefaultAzureCredential
from azure.identity.aio import DefaultAzureCredential as AsyncDefaultAzureCredential

from pyrannic.contracts import ConfigRepositoryInterface
from pyrannic.contracts.database import AsyncAuthTypeInterface, AuthTypeInterface
from pyrannic.ioc import Resolves


class EntraAuthType(AuthTypeInterface):
    def __init__(self, config: Resolves[ConfigRepositoryInterface]):
        self._config = config
        self._credential = DefaultAzureCredential()
        self._password = None

    @property
    def password(self) -> str | None:
        if not self._password:
            self.fetch_password()

        return self._password

    def fetch_password(self) -> None:
        token_scope = self._config.str("azure.database.token_scope")
        access_token = self._credential.get_token(token_scope)
        self._password = access_token.token

    def close(self) -> None:
        self._credential.close()


class AsyncEntraAuthType(AsyncAuthTypeInterface):
    def __init__(self, config: Resolves[ConfigRepositoryInterface]):
        self._config = config
        self._credential = AsyncDefaultAzureCredential()
        self._password = None

    @property
    def password(self) -> str | None:
        return self._password

    async def fetch_password(self):
        token_scope = self._config.str("azure.database.token_scope")
        access_token = await self._credential.get_token(token_scope)
        self._password = access_token.token

    async def close(self) -> None:
        await self._credential.close()
