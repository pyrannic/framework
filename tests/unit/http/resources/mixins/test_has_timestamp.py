from datetime import datetime

from tests.unit.http.resources.utils import HasTimestampResource


def test_has_timestamp():
    created_at = datetime.now()

    resource = HasTimestampResource(
        id=1,
        name="Test Resource",
        created_at=created_at,
    )

    assert resource.created_at == created_at


def test_has_timestamp__serialize():
    created_at = datetime(2026, 1, 1)

    resource = HasTimestampResource(
        id=1,
        name="Test Resource",
        created_at=created_at,
    )

    assert resource.model_dump(mode="json") == {
        "id": 1,
        "name": "Test Resource",
        "created_at": "2026-01-01T00:00:00.000Z",
    }
