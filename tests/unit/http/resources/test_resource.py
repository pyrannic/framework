from datetime import datetime

from tests.unit.http.resources.utils import (
    FooModel,
    FooResource,
    FooResourceWithRelationships,
)


def test_resource():
    created_at = datetime.now()

    resource = FooResource(
        id=1,
        name="Test Resource",
        created_at=created_at,
        updated_at=created_at,
    )

    assert resource.id == 1
    assert resource.name == "Test Resource"
    assert resource.created_at == created_at
    assert resource.updated_at == created_at


def test_has_timestamps__serialize():
    created_at = datetime(2026, 1, 1)

    resource = FooResource(
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
        "deleted_at": None,
    }


def test_has_timestamps__to_dict():
    created_at = datetime(2026, 1, 1)

    resource = FooResource(
        id=1,
        name="Test Resource",
        created_at=created_at,
        updated_at=created_at,
    )

    assert resource.to_dict() == {
        "id": 1,
        "name": "Test Resource",
        "created_at": created_at,
        "updated_at": created_at,
        "deleted_at": None,
    }


def test_resource__from_model():
    created_at = datetime(2026, 1, 1)

    resource = FooResource.from_model(
        FooModel(
            id=1,
            name="Test Resource",
            created_at=created_at,
            updated_at=created_at,
        )
    )

    assert resource.to_dict() == {
        "id": 1,
        "name": "Test Resource",
        "created_at": created_at,
        "updated_at": created_at,
        "deleted_at": None,
    }


def test_resource__model_to_dict():
    created_at = datetime(2026, 1, 1)

    assert FooResource.model_to_dict(
        FooModel(
            id=1,
            name="Test Resource",
            created_at=created_at,
            updated_at=created_at,
        )
    ) == {
        "id": 1,
        "name": "Test Resource",
        "created_at": created_at,
        "updated_at": created_at,
        "deleted_at": None,
    }


def test_resource__model_to_dict_no_relationships():
    created_at = datetime(2026, 1, 1)

    model = FooModel(
        id=1,
        name="Test Resource",
        created_at=created_at,
        updated_at=created_at,
    )

    FooResourceWithRelationships.from_model(model, with_relationships=False)

    assert FooResourceWithRelationships.model_to_dict(model) == {
        "id": 1,
        "name": "Test Resource",
        "created_at": created_at,
        "updated_at": created_at,
        "deleted_at": None,
    }


def test_resource__model_to_dict_empty_relationship():
    created_at = datetime(2026, 1, 1)

    model = FooModel(
        id=1,
        name="Test Resource",
        created_at=created_at,
        updated_at=created_at,
    )

    FooResourceWithRelationships.from_model(model)

    assert FooResourceWithRelationships.model_to_dict(model) == {
        "id": 1,
        "name": "Test Resource",
        "created_at": created_at,
        "updated_at": created_at,
        "deleted_at": None,
        "children": [],
    }


def test_resource__model_to_dict_only_with_children_relationship():
    created_at = datetime(2026, 1, 1)

    model = FooModel(
        id=1,
        name="Test Resource",
        created_at=created_at,
        updated_at=created_at,
    )

    FooResourceWithRelationships.from_model(model, with_relationships=["children"])

    assert FooResourceWithRelationships.model_to_dict(model) == {
        "id": 1,
        "name": "Test Resource",
        "created_at": created_at,
        "updated_at": created_at,
        "deleted_at": None,
        "children": [],
    }


def test_resource__model_to_dict_with_relationships():
    created_at = datetime(2026, 1, 1)

    child_1 = FooModel(
        id=2,
        name="Child Resource",
        created_at=created_at,
        updated_at=created_at,
    )

    assert FooResourceWithRelationships.model_to_dict(
        FooModel(
            id=1,
            name="Test Resource",
            created_at=created_at,
            updated_at=created_at,
            children=[child_1],
        )
    ) == {
        "id": 1,
        "name": "Test Resource",
        "created_at": created_at,
        "updated_at": created_at,
        "deleted_at": None,
        "children": [FooResourceWithRelationships.from_model(child_1)],
    }
