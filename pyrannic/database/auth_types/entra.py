from typing import Any

from azure.identity import DefaultAzureCredential
from azure.identity.aio import DefaultAzureCredential as AsyncDefaultAzureCredential

from pyrannic.contracts import ConfigRepositoryInterface
from pyrannic.contracts.database import AuthTypeInterface
from pyrannic.ioc import Resolves


class EntraAuthType(AuthTypeInterface):
    def __init__(self, config: Resolves[ConfigRepositoryInterface]):
        self._config = config
        self._credential = DefaultAzureCredential()

    @property
    def password(self) -> str | Any | None:
        token_scope = self._config.str("azure.database.token_scope")
        access_token = self._credential.get_token(token_scope)

        return access_token

    def close(self) -> None:
        self._credential.close()


class AsyncEntraAuthType(AuthTypeInterface):
    def __init__(self, config: Resolves[ConfigRepositoryInterface]):
        self._config = config
        self._credential = AsyncDefaultAzureCredential()

    @property
    async def password(self) -> str | Any | None:
        token_scope = self._config.str("azure.database.token_scope")
        access_token = await self._credential.get_token(token_scope)

        return access_token

    async def close(self) -> None:
        await self._credential.close()
