import pytest

from pyrannic.contracts import ApplicationInterface
from pyrannic.contracts.database.manager import DatabaseManagerInterface
from pyrannic.contracts.orm import RepositoryInterface
from tests.unit.orm.sqlalchemy.utils import BarModel, BarsTable


def test_tablename_property():
    assert BarModel.tablename() == "bars"
    assert BarModel.__tablename__ == "bars"


def test_primary_key_column():
    assert BarModel.primary_key_column().name == "id"  # pyright: ignore[reportFunctionMemberAccess, reportUnknownMemberType, reportAttributeAccessIssue]


def test_primary_key_value():
    bar = BarModel(id=1)
    assert bar.primary_key_value == 1


@pytest.mark.asyncio
async def test_is_dirty_and_is_clean(
    application: ApplicationInterface,
    repository: RepositoryInterface[BarModel],
):
    manager = await application.container.resolve(DatabaseManagerInterface)
    await manager.migrate([BarsTable])

    bar = BarModel(id=1, name="Bar")

    # Initially, the model is not saved, so it should be considered dirty
    assert bar.is_dirty()
    assert not bar.is_clean()

    # Save the model to the repository
    bar = repository.create(bar)
    assert not bar.is_dirty()
    assert bar.is_clean()

    # Simulate a change to the model
    bar.id = 2
    assert bar.is_dirty()
    assert not bar.is_clean()

    # Check specific attribute
    assert bar.is_dirty("id")
    assert not bar.is_clean("id")

    # Check with an attribute that hasn't changed
    assert not bar.is_dirty("name")
    assert not bar.is_dirty("non_existent_attr")
