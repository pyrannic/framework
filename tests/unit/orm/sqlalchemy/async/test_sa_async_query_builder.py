import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from pyrannic.contracts.application import ApplicationInterface
from pyrannic.orm.sqlalchemy import (
    AsyncRepository,
)
from tests.unit.orm.sqlalchemy.utils import BarModel


@pytest.mark.asyncio
async def test_async_query_builder(application: ApplicationInterface):
    repository = await application.container.resolve(AsyncRepository[BarModel])
    assert isinstance(repository.session, AsyncSession)
