from datetime import datetime

from tests.unit.http.resources.utils import HasTimestampsResource


def test_has_timestamps():
    created_at = datetime.now()

    resource = HasTimestampsResource(
        id=1,
        name="Test Resource",
        created_at=created_at,
        updated_at=created_at,
    )

    assert resource.created_at == created_at
    assert resource.updated_at == created_at


def test_has_timestamps__serialize():
    created_at = datetime(2026, 1, 1)

    resource = HasTimestampsResource(
        id=1,
        name="Test Resource",
        created_at=created_at,
        updated_at=created_at,
    )

    assert resource.model_dump(mode="json") == {
        "id": 1,
        "name": "Test Resource",
        "created_at": "2026-01-01T00:00:00.000Z",
        "updated_at": "2026-01-01T00:00:00.000Z",
    }
