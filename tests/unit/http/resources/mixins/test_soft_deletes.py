from datetime import datetime

from tests.unit.http.resources.utils import SoftDeletesResource


def test_soft_deletes():
    deleted_at = datetime.now()

    resource = SoftDeletesResource(
        id=1,
        name="Test Resource",
        deleted_at=deleted_at,
    )

    assert resource.deleted_at == deleted_at


def test_soft_deletes__serialize():
    deleted_at = datetime(2026, 1, 1)

    resource = SoftDeletesResource(
        id=1,
        name="Test Resource",
        deleted_at=deleted_at,
    )

    assert resource.model_dump(mode="json") == {
        "id": 1,
        "name": "Test Resource",
        "deleted_at": "2026-01-01T00:00:00.000Z",
    }


def test_soft_deletes__serialize_with_none():
    resource = SoftDeletesResource(id=1, name="Test Resource")

    assert resource.model_dump(mode="json") == {
        "id": 1,
        "name": "Test Resource",
        "deleted_at": None,
    }
