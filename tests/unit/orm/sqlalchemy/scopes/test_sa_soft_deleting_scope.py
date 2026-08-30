import pytest

from pyrannic.contracts import ApplicationInterface, DatabaseManagerInterface
from tests.unit.orm.sqlalchemy.utils import (
    FooModel,
    FooRepository,
    FoosTable,
)


@pytest.mark.asyncio
async def test_with_removed(application: ApplicationInterface) -> None:
    manager = await application.container.resolve(DatabaseManagerInterface)
    repository = await application.container.make(FooRepository)

    await manager.rollback([FoosTable])
    await manager.migrate([FoosTable])

    repository.create(FooModel())
    repository.create(FooModel())
    model = repository.create(FooModel())
    repository.remove(model)

    count = repository.with_removed().count()

    assert count == 3


@pytest.mark.asyncio
async def test_only_removed(application: ApplicationInterface) -> None:
    manager = await application.container.resolve(DatabaseManagerInterface)
    repository = await application.container.make(FooRepository)

    await manager.rollback([FoosTable])
    await manager.migrate([FoosTable])

    repository.create(FooModel())
    repository.create(FooModel())
    model = repository.create(FooModel())
    repository.remove(model)

    count = repository.only_removed().count()

    assert count == 1


@pytest.mark.asyncio
async def test_reset_after_query(application: ApplicationInterface) -> None:
    manager = await application.container.resolve(DatabaseManagerInterface)
    repository = await application.container.make(FooRepository)

    await manager.rollback([FoosTable])
    await manager.migrate([FoosTable])

    repository.create(FooModel())
    repository.create(FooModel())
    model = repository.create(FooModel())
    repository.remove(model)

    db_model = repository.only_removed().first()
    count = repository.count()

    assert db_model == model
    assert count == 2
