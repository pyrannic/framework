from datetime import datetime

from tests.unit.orm.sqlalchemy.utils import SoftDeletesModel


def test_initial_deleted_at() -> None:
    model = SoftDeletesModel()
    assert model.deleted_at is None


def test_set_deleted_at() -> None:
    model = SoftDeletesModel()
    assert model.deleted_at is None

    new_deleted_at = datetime(2024, 1, 1, 12, 0, 0)
    model.set_deleted_at(new_deleted_at)
    assert model.deleted_at == new_deleted_at


def test_is_deleted_property() -> None:
    model = SoftDeletesModel()
    assert model.is_deleted is False

    model.set_deleted_at(datetime(2024, 1, 1, 12, 0, 0))
    assert model.is_deleted is True


def test_deleted_at_column_name() -> None:
    assert SoftDeletesModel.deleted_at_column() == "deleted_at"
