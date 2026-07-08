from typing import Annotated, Any, AsyncGenerator, Generator

from fastapi import Depends

from pyrannic.container.param_functions import Resolves
from pyrannic.contracts.database.manager import DatabaseManagerInterface

from sqlalchemy.ext.asyncio import AsyncSession as _AsyncSession
from sqlalchemy.orm import Session as _Session


def get_session(
    manager: Annotated[DatabaseManagerInterface, Resolves()],
) -> Generator[Any, Any, _Session | None]:
    with manager.connection() as session:
        yield session


async def get_async_session(
    manager: Annotated[DatabaseManagerInterface, Resolves()],
) -> AsyncGenerator[Any, _AsyncSession]:
    async with manager.connection() as session:
        yield session


AsyncSession = Annotated[_AsyncSession, Depends(get_async_session)]
Session = Annotated[_Session, Depends(get_session)]
