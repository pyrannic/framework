import pytest
from sqlalchemy.orm import Session

from pyrannic.contracts.application import ApplicationInterface
from pyrannic.orm.sqlalchemy import (
    Repository,
)
from tests.unit.orm.sqlalchemy.utils import BarModel


@pytest.mark.asyncio
async def test_query_builder(application: ApplicationInterface):
    repository = await application.container.resolve(Repository[BarModel])
    assert isinstance(repository.session, Session)
