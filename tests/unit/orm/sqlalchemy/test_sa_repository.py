import pytest

from pyrannic.contracts.application import ApplicationInterface
from pyrannic.orm.sqlalchemy import (
    Repository,
)
from tests.unit.orm.sqlalchemy.utils import BarModel


@pytest.mark.asyncio
async def test_model(application: ApplicationInterface):
    repository = await application.container.resolve(Repository[BarModel])
    assert repository.model == BarModel
