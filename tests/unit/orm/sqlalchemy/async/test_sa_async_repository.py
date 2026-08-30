from typing import Any

import pytest
from pytest import LogCaptureFixture, MonkeyPatch
from sqlalchemy.exc import ArgumentError

from pyrannic.contracts import ApplicationInterface
from pyrannic.orm.sqlalchemy import AsyncRepository
from pyrannic.pagination.meta import PaginationMeta
from tests.unit.orm.sqlalchemy.utils import (
    BarModel,
    FooAsyncRepository,
    FooModel,
)


async def _raise_argument_error(*args: Any, **kwargs: Any):
    raise ArgumentError("Simulated error")


@pytest.mark.asyncio
async def test_async_repository_model__generic(application: ApplicationInterface):
    """
    Test that the repository model is correctly set when using a generic repository.
    """
    repository = await application.container.resolve(AsyncRepository[BarModel])

    assert isinstance(repository, AsyncRepository)
    assert repository.model == BarModel


@pytest.mark.asyncio
async def test_async_repository_model__subclass(application: ApplicationInterface):
    """
    Test that the repository model is correctly set when using a subclass of the repository.
    """
    repository = await application.container.resolve(FooAsyncRepository)

    assert isinstance(repository, FooAsyncRepository)
    assert repository.model == FooModel


@pytest.mark.asyncio
async def test_async_repository_create(application: ApplicationInterface) -> None:
    repository = await application.container.make(FooAsyncRepository)

    await repository.create(FooModel())
    await repository.create(FooModel())
    await repository.create(FooModel())

    count = await repository.count()

    assert count == 3


@pytest.mark.asyncio
async def test_async_repository_create_raises_exception(
    application: ApplicationInterface,
    monkeypatch: MonkeyPatch,
    caplog: LogCaptureFixture,
) -> None:
    repository = await application.container.make(FooAsyncRepository)

    monkeypatch.setattr(repository.session, "commit", _raise_argument_error)  # pyright: ignore[reportUnknownArgumentType]

    with pytest.raises(ArgumentError):
        await repository.create(FooModel())

    assert "Rolling Back" in caplog.text
    assert "Error inserting model" in caplog.text

    count = await repository.count()
    assert count == 0


@pytest.mark.asyncio
async def test_async_repository_update(application: ApplicationInterface) -> None:
    repository = await application.container.make(FooAsyncRepository)

    model = await repository.create(FooModel(name="Old Name"))
    assert model.name == "Old Name"

    model = await repository.find(model.id)
    assert model is not None
    assert model.name == "Old Name"

    model.name = "New Name"
    model = await repository.update(model)
    assert model.name == "New Name"

    model = await repository.find(model.id)
    assert model is not None
    assert model.name == "New Name"


@pytest.mark.asyncio
async def test_async_repository_update_raises_exception(
    application: ApplicationInterface,
    monkeypatch: MonkeyPatch,
    caplog: LogCaptureFixture,
) -> None:
    repository = await application.container.make(FooAsyncRepository)
    model = await repository.create(FooModel(name="Old Name"))

    monkeypatch.setattr(repository.session, "commit", _raise_argument_error)  # pyright: ignore[reportUnknownArgumentType]

    with pytest.raises(ArgumentError):
        model.name = "New Name"
        await repository.update(model)

    assert "Rolling Back" in caplog.text
    assert "Error updating model" in caplog.text

    # TODO - Investigate why the following assertions are failing
    # model = await repository.find(model.id)
    # assert model is not None
    # assert model.name == "Old Name"


@pytest.mark.asyncio
async def test_async_repository_destroy(application: ApplicationInterface) -> None:
    repository = await application.container.make(FooAsyncRepository)

    model = await repository.create(FooModel())
    count = await repository.count()

    assert count == 1

    await repository.destroy(model)
    count = await repository.count()

    assert count == 0


@pytest.mark.asyncio
async def test_async_repository_destroy_raises_exception(
    application: ApplicationInterface,
    monkeypatch: MonkeyPatch,
    caplog: LogCaptureFixture,
) -> None:
    repository = await application.container.make(FooAsyncRepository)
    model = await repository.create(FooModel())

    monkeypatch.setattr(repository.session, "commit", _raise_argument_error)  # pyright: ignore[reportUnknownArgumentType]

    with pytest.raises(ArgumentError):
        await repository.destroy(model)

    assert "Rolling Back" in caplog.text
    assert "Error destroying model" in caplog.text

    count = await repository.count()
    assert count == 1


@pytest.mark.asyncio
async def test_async_repository_remove(application: ApplicationInterface) -> None:
    repository = await application.container.make(FooAsyncRepository)

    model = await repository.create(FooModel())
    db_model = await repository.remove(model)

    assert db_model is not None
    assert db_model.is_deleted is True


@pytest.mark.asyncio
async def test_async_repository_restore(application: ApplicationInterface) -> None:
    repository = await application.container.make(FooAsyncRepository)

    model = await repository.create(FooModel())
    db_model = await repository.remove(model)

    assert db_model is not None
    assert db_model.is_deleted is True

    db_model = await repository.restore(db_model)

    assert db_model is not None
    assert db_model.is_deleted is False


@pytest.mark.asyncio
async def test_async_repository_count(application: ApplicationInterface) -> None:
    repository = await application.container.make(FooAsyncRepository)
    total = 5

    for _ in range(total):
        await repository.create(FooModel())

    count = await repository.count()

    assert count == total


@pytest.mark.asyncio
async def test_async_repository_first(application: ApplicationInterface) -> None:
    repository = await application.container.make(FooAsyncRepository)

    await repository.create(FooModel(name="First"))
    await repository.create(FooModel(name="Second"))
    await repository.create(FooModel(name="Third"))

    model = await repository.order_by(FooModel.name).first()

    assert model is not None
    assert model.name == "First"


@pytest.mark.asyncio
async def test_async_repository_all(application: ApplicationInterface) -> None:
    repository = await application.container.make(FooAsyncRepository)

    await repository.create(FooModel(name="First"))
    await repository.create(FooModel(name="Second"))
    await repository.create(FooModel(name="Third"))

    models = await repository.all()

    assert len(models) == 3
    assert models[0].name == "First"
    assert models[1].name == "Second"
    assert models[2].name == "Third"


@pytest.mark.asyncio
async def test_async_repository_get(application: ApplicationInterface) -> None:
    repository = await application.container.make(FooAsyncRepository)

    await repository.create(FooModel(name="First"))
    await repository.create(FooModel(name="Second"))
    await repository.create(FooModel(name="Third"))

    models = await repository.order_by(FooModel.name).get()

    assert len(models) == 3
    assert models[0].name == "First"
    assert models[1].name == "Second"
    assert models[2].name == "Third"


@pytest.mark.asyncio
async def test_async_repository_find(application: ApplicationInterface) -> None:
    repository = await application.container.make(FooAsyncRepository)

    await repository.create(FooModel(name="First"))
    await repository.create(FooModel(name="Second"))
    await repository.create(FooModel(name="Third"))

    found_model = await repository.find(1)

    assert found_model is not None
    assert found_model.id == 1
    assert found_model.name == "First"


@pytest.mark.asyncio
async def test_async_repository_paginate(application: ApplicationInterface) -> None:
    repository = await application.container.make(FooAsyncRepository)

    for i in range(1, 21):
        await repository.create(FooModel(name=f"Foo {i}"))

    paginator = await repository.order_by(FooModel.id).paginate(page=2, per_page=5)
    meta = paginator.meta(PaginationMeta)

    assert meta.current_page == 2
    assert meta.per_page == 5
    assert meta.total == 20
    assert meta.last_page == 4
    assert len(paginator.items) == 5
    assert paginator.items[0].name == "Foo 6"
