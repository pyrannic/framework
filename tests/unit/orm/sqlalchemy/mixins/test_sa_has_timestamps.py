from datetime import datetime, timezone

from pyrannic.support.datetime import get_current_utc_datetime
from tests.unit.orm.sqlalchemy.utils import HasTimestampsModel


def test_initial_created_at() -> None:
    created_at = get_current_utc_datetime()
    model = HasTimestampsModel()

    assert model.created_at.tzinfo == timezone.utc
    assert abs((model.created_at - created_at).total_seconds()) < 1


def test_set_created_at() -> None:
    model = HasTimestampsModel()
    assert model.created_at is not None

    new_created_at = datetime(2024, 1, 1, 12, 0, 0)
    model.set_created_at(new_created_at)
    assert model.created_at == new_created_at


def test_initial_updated_at() -> None:
    updated_at = get_current_utc_datetime()
    model = HasTimestampsModel()

    assert model.updated_at.tzinfo == timezone.utc
    assert abs((model.updated_at - updated_at).total_seconds()) < 1


def test_set_updated_at() -> None:
    model = HasTimestampsModel()
    assert model.updated_at is not None

    new_updated_at = datetime(2024, 1, 1, 12, 0, 0)
    model.set_updated_at(new_updated_at)
    assert model.updated_at == new_updated_at
