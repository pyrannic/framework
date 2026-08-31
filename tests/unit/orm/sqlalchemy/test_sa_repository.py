import pytest
from pytest import LogCaptureFixture, MonkeyPatch
from sqlalchemy.exc import ArgumentError

from pyrannic.contracts import ApplicationInterface
from pyrannic.orm.sqlalchemy import Repository
from pyrannic.pagination.meta import PaginationMeta
from tests.unit.orm.sqlalchemy.utils import (
    BarModel,
    BazModel,
    BazRepository,
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
async def test_repository_raises_value_error(
    application: ApplicationInterface,
):
    with pytest.raises(ValueError) as exc_info:
        await application.container.resolve(Repository)

    error = str(exc_info.value)
    assert "The model type could not be determined" in error
    assert "class is properly typed with a generic model" in error
    assert "explicitly set the '__model__' attribute in the subclass" in error


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
async def test_repository_try_remove_no_soft_delete_model(
    application: ApplicationInterface,
) -> None:
    repository = await application.container.make(BazRepository)

    model = repository.create(BazModel())
    db_model = repository.remove(model)

    assert db_model is not None
    assert db_model == model
    assert repository.find(model.id) == db_model == model


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

    paginator = repository.paginate(page=2, per_page=5)
    meta = paginator.meta(PaginationMeta)

    assert meta.current_page == 2
    assert meta.per_page == 5
    assert meta.total == 20
    assert meta.last_page == 4
    assert len(paginator.items) == 5
    assert paginator.items[0].name == "Foo 6"


@pytest.mark.asyncio
async def test_repository_paginate_no_per_page(
    application: ApplicationInterface,
) -> None:
    repository = await application.container.make(FooRepository)

    for i in range(1, 21):
        repository.create(FooModel(name=f"Foo {i}"))

    paginator = repository.paginate(page=2)
    meta = paginator.meta(PaginationMeta)

    assert meta.current_page == 1
    assert meta.per_page == 20
    assert meta.total == 20
    assert meta.last_page == 1
    assert len(paginator.items) == 20
    assert paginator.items[0].name == "Foo 1"


@pytest.mark.asyncio
async def test_repository_paginate_negative_per_page(
    application: ApplicationInterface,
) -> None:
    repository = await application.container.make(FooRepository)

    for i in range(1, 21):
        repository.create(FooModel(name=f"Foo {i}"))

    paginator = repository.paginate(page=2, per_page=-5)
    meta = paginator.meta(PaginationMeta)

    assert meta.current_page == 1
    assert meta.per_page == 20
    assert meta.total == 20
    assert meta.last_page == 1
    assert len(paginator.items) == 20
    assert paginator.items[0].name == "Foo 1"


@pytest.mark.asyncio
async def test_repository_paginate_negative_page(
    application: ApplicationInterface,
) -> None:
    repository = await application.container.make(FooRepository)

    for i in range(1, 21):
        repository.create(FooModel(name=f"Foo {i}"))

    paginator = repository.paginate(page=-12, per_page=15)
    meta = paginator.meta(PaginationMeta)

    assert meta.current_page == 1
    assert meta.per_page == 15
    assert meta.total == 20
    assert meta.last_page == 2
    assert len(paginator.items) == 15
    assert paginator.items[0].name == "Foo 1"


@pytest.mark.asyncio
async def test_repository_paginate_page_is_none(
    application: ApplicationInterface,
) -> None:
    repository = await application.container.make(FooRepository)

    for i in range(1, 21):
        repository.create(FooModel(name=f"Foo {i}"))

    paginator = repository.paginate(page=None, per_page=15)  # pyright: ignore[reportArgumentType]
    meta = paginator.meta(PaginationMeta)

    assert meta.current_page == 1
    assert meta.per_page == 15
    assert meta.total == 20
    assert meta.last_page == 2
    assert len(paginator.items) == 15
    assert paginator.items[0].name == "Foo 1"


@pytest.mark.asyncio
async def test_repository_paginate_resolve_last_page(
    application: ApplicationInterface,
) -> None:
    repository = await application.container.make(FooRepository)

    assert repository._resolve_last_page() == 1  # pyright: ignore[reportPrivateUsage]
    assert repository._resolve_last_page(-20) == 1  # pyright: ignore[reportPrivateUsage]


@pytest.mark.asyncio
async def test_repository_where_kwargs(application: ApplicationInterface) -> None:
    repository = await application.container.make(FooRepository)

    for i in range(1, 21):
        repository.create(FooModel(name=f"Foo {i}"))

    models = repository.where(name="Foo 1").get()

    assert len(models) == 1
    assert models[0].name == "Foo 1"


@pytest.mark.asyncio
async def test_repository_filter_with_filters(
    application: ApplicationInterface,
) -> None:
    repository = await application.container.make(FooRepository)

    for i in range(1, 21):
        repository.create(FooModel(name=f"Foo {i}"))

    models = repository.filter(FooModel.name == "Foo 1").get()

    assert len(models) == 1
    assert models[0].name == "Foo 1"


@pytest.mark.asyncio
async def test_repository_filter_kwargs(application: ApplicationInterface) -> None:
    repository = await application.container.make(FooRepository)

    for i in range(1, 21):
        repository.create(FooModel(name=f"Foo {i}"))

    models = repository.filter(name="Foo 1").get()

    assert len(models) == 1
    assert models[0].name == "Foo 1"


@pytest.mark.asyncio
async def test_repository_group_by(application: ApplicationInterface) -> None:
    repository = await application.container.make(FooRepository)

    for _ in range(1, 21):
        repository.create(FooModel(name="Foo"))

    models = repository.group_by(FooModel.name).get()

    assert len(models) == 1
    assert models[0].name == "Foo"


@pytest.mark.asyncio
async def test_repository_join(application: ApplicationInterface) -> None:
    repository = await application.container.make(FooRepository)
    repository.join(BazModel).get()

    # TODO: Add assertions to verify the join behavior.
