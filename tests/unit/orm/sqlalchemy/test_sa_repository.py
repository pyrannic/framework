import pytest
from pytest import LogCaptureFixture, MonkeyPatch
from sqlalchemy.exc import ArgumentError

from pyrannic.contracts import ApplicationInterface
from pyrannic.orm.sqlalchemy import Repository
from pyrannic.pagination.meta import PaginationMeta
from tests.unit.orm.sqlalchemy.utils import (
    BarModel,
    FooModel,
    FooRepository,
)


@pytest.mark.asyncio
async def test_repository_model__generic(application: ApplicationInterface):
    """
    Test that the repository model is correctly set when using a generic repository.
    """
    repository = await application.container.resolve(Repository[BarModel])

    assert isinstance(repository, Repository)
    assert repository.model == BarModel


@pytest.mark.asyncio
async def test_repository_model__subclass(application: ApplicationInterface):
    """
    Test that the repository model is correctly set when using a subclass of the repository.
    """
    repository = await application.container.resolve(FooRepository)

    assert isinstance(repository, FooRepository)
    assert repository.model == FooModel


@pytest.mark.asyncio
async def test_repository_create(application: ApplicationInterface) -> None:
    repository = await application.container.make(FooRepository)

    repository.create(FooModel())
    repository.create(FooModel())
    repository.create(FooModel())

    count = repository.count()

    assert count == 3


@pytest.mark.asyncio
async def test_repository_create_raises_exception(
    application: ApplicationInterface,
    monkeypatch: MonkeyPatch,
    caplog: LogCaptureFixture,
) -> None:
    repository = await application.container.make(FooRepository)

    monkeypatch.setattr(
        repository.session,
        "commit",
        lambda *args, **kwargs: (_ for _ in ()).throw(ArgumentError),  # type: ignore
    )

    with pytest.raises(ArgumentError):
        repository.create(FooModel())

    assert "Rolling Back" in caplog.text
    assert "Error inserting model" in caplog.text

    count = repository.count()
    assert count == 0


@pytest.mark.asyncio
async def test_repository_update(application: ApplicationInterface) -> None:
    repository = await application.container.make(FooRepository)

    model = repository.create(FooModel(name="Old Name"))
    assert model.name == "Old Name"

    model = repository.find(model.id)
    assert model is not None
    assert model.name == "Old Name"

    model.name = "New Name"
    model = repository.update(model)
    assert model.name == "New Name"

    model = repository.find(model.id)
    assert model is not None
    assert model.name == "New Name"


@pytest.mark.asyncio
async def test_repository_update_raises_exception(
    application: ApplicationInterface,
    monkeypatch: MonkeyPatch,
    caplog: LogCaptureFixture,
) -> None:
    repository = await application.container.make(FooRepository)

    model = repository.create(FooModel(name="Old Name"))

    monkeypatch.setattr(
        repository.session,
        "commit",
        lambda *args, **kwargs: (_ for _ in ()).throw(ArgumentError),  # type: ignore
    )

    with pytest.raises(ArgumentError):
        model.name = "New Name"
        repository.update(model)

    assert "Rolling Back" in caplog.text
    assert "Error updating model" in caplog.text

    model = repository.find(model.id)
    assert model is not None
    assert model.name == "Old Name"


@pytest.mark.asyncio
async def test_repository_destroy(application: ApplicationInterface) -> None:
    repository = await application.container.make(FooRepository)

    model = repository.create(FooModel())
    count = repository.count()

    assert count == 1

    repository.destroy(model)
    count = repository.count()

    assert count == 0


@pytest.mark.asyncio
async def test_repository_destroy_raises_exception(
    application: ApplicationInterface,
    monkeypatch: MonkeyPatch,
    caplog: LogCaptureFixture,
) -> None:
    repository = await application.container.make(FooRepository)
    model = repository.create(FooModel())

    monkeypatch.setattr(
        repository.session,
        "commit",
        lambda *args, **kwargs: (_ for _ in ()).throw(ArgumentError),  # type: ignore
    )

    with pytest.raises(ArgumentError):
        repository.destroy(model)

    assert "Rolling Back" in caplog.text
    assert "Error destroying model" in caplog.text

    count = repository.count()
    assert count == 1


@pytest.mark.asyncio
async def test_repository_remove(application: ApplicationInterface) -> None:
    repository = await application.container.make(FooRepository)

    model = repository.create(FooModel())
    db_model = repository.remove(model)

    assert db_model is not None
    assert db_model.is_deleted is True


@pytest.mark.asyncio
async def test_repository_restore(application: ApplicationInterface) -> None:
    repository = await application.container.make(FooRepository)

    model = repository.create(FooModel())
    db_model = repository.remove(model)

    assert db_model is not None
    assert db_model.is_deleted is True

    db_model = repository.restore(db_model)

    assert db_model is not None
    assert db_model.is_deleted is False


@pytest.mark.asyncio
async def test_repository_count(application: ApplicationInterface) -> None:
    repository = await application.container.make(FooRepository)
    total = 5

    for _ in range(total):
        repository.create(FooModel())

    count = repository.count()

    assert count == total


@pytest.mark.asyncio
async def test_repository_first(application: ApplicationInterface) -> None:
    repository = await application.container.make(FooRepository)

    repository.create(FooModel(name="First"))
    repository.create(FooModel(name="Second"))
    repository.create(FooModel(name="Third"))

    model = repository.order_by(FooModel.name).first()

    assert model is not None
    assert model.name == "First"


@pytest.mark.asyncio
async def test_repository_all(application: ApplicationInterface) -> None:
    repository = await application.container.make(FooRepository)

    repository.create(FooModel(name="First"))
    repository.create(FooModel(name="Second"))
    repository.create(FooModel(name="Third"))

    models = repository.all()

    assert len(models) == 3
    assert models[0].name == "First"
    assert models[1].name == "Second"
    assert models[2].name == "Third"


@pytest.mark.asyncio
async def test_repository_get(application: ApplicationInterface) -> None:
    repository = await application.container.make(FooRepository)

    repository.create(FooModel(name="First"))
    repository.create(FooModel(name="Second"))
    repository.create(FooModel(name="Third"))

    models = repository.order_by(FooModel.name).get()

    assert len(models) == 3
    assert models[0].name == "First"
    assert models[1].name == "Second"
    assert models[2].name == "Third"


@pytest.mark.asyncio
async def test_repository_find(application: ApplicationInterface) -> None:
    repository = await application.container.make(FooRepository)

    repository.create(FooModel(name="First"))
    repository.create(FooModel(name="Second"))
    repository.create(FooModel(name="Third"))

    found_model = repository.find(1)

    assert found_model is not None
    assert found_model.id == 1
    assert found_model.name == "First"


@pytest.mark.asyncio
async def test_repository_paginate(application: ApplicationInterface) -> None:
    repository = await application.container.make(FooRepository)

    for i in range(1, 21):
        repository.create(FooModel(name=f"Foo {i}"))

    paginator = repository.order_by(FooModel.id).paginate(page=2, per_page=5)
    meta = paginator.meta(PaginationMeta)

    assert meta.current_page == 2
    assert meta.per_page == 5
    assert meta.total == 20
    assert meta.last_page == 4
    assert len(paginator.items) == 5
    assert paginator.items[0].name == "Foo 6"
