from datetime import datetime

import pytest

from pyrannic.contracts import ApplicationInterface, DatabaseManagerInterface
from tests.unit.orm.sqlalchemy.utils import (
    FooModel,
    FooRepository,
    FoosTable,
)


def test_initial_deleted_at() -> None:
    model = FooModel()
    assert model.deleted_at is None


def test_set_deleted_at() -> None:
    model = FooModel()
    assert model.deleted_at is None

    new_deleted_at = datetime(2024, 1, 1, 12, 0, 0)
    model.set_deleted_at(new_deleted_at)
    assert model.deleted_at == new_deleted_at


def test_is_deleted_property() -> None:
    model = FooModel()
    assert model.is_deleted is False

    model.set_deleted_at(datetime(2024, 1, 1, 12, 0, 0))
    assert model.is_deleted is True


def test_deleted_at_column_name() -> None:
    assert FooModel.deleted_at_column() == "deleted_at"


@pytest.mark.asyncio
async def test_is_deleted_inplace_expression(application: ApplicationInterface) -> None:
    model = FooModel()
    manager = await application.container.resolve(DatabaseManagerInterface)
    repository = await application.container.make(FooRepository)

    await manager.migrate([FoosTable])

    model = repository.create(model)
    repository.remove(model)

    count = repository.with_removed().where(FooModel.is_deleted).count()

    assert count == 1


@pytest.mark.asyncio
async def test_create_a_model_deleted(application: ApplicationInterface) -> None:
    date = datetime(2024, 1, 1, 12, 0, 0)
    model = FooModel()
    model.set_deleted_at(date)

    manager = await application.container.resolve(DatabaseManagerInterface)
    repository = await application.container.make(FooRepository)

    await manager.migrate([FoosTable])

    model = repository.create(model)

    assert model.id is not None
    assert model.deleted_at == date
    assert model.is_deleted is True
