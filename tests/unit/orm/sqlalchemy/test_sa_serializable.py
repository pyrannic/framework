from tests.unit.orm.sqlalchemy.utils import BarModel


def test_to_dict():
    bar = BarModel(id=1, name="Bar")
    data = bar.to_dict()

    assert data == {"id": 1, "name": "Bar", "parent_id": None, "upper_name": "BAR"}


def test_to_dict_with_exclude():
    bar = BarModel(id=1, name="Bar")
    data = bar.to_dict(exclude=["name"])

    assert data == {"id": 1, "parent_id": None, "upper_name": "BAR"}


def test_to_dict_with_hybrid_property():
    bar = BarModel(id=1, name="BarBarBar")
    data = bar.to_dict(hybrid_attributes=True)

    assert data == {
        "id": 1,
        "name": "BarBarBar",
        "slug": "bar-bar-bar",
        "parent_id": None,
        "upper_name": "BARBARBAR",
    }


def test_to_dict_with_exclude_and_hybrid_property():
    bar = BarModel(id=1, name="BarBarBar")
    data = bar.to_dict(exclude=["name"], hybrid_attributes=True)

    assert data == {
        "id": 1,
        "slug": "bar-bar-bar",
        "parent_id": None,
        "upper_name": "BARBARBAR",
    }


def test_to_dict_with_missing_exclude():
    bar = BarModel(id=1, name="Bar")
    data = bar.to_dict(exclude=["non_existent_property"])

    assert data == {"id": 1, "name": "Bar", "parent_id": None, "upper_name": "BAR"}


def test_to_dict_with_nested_relationship():
    bar1 = BarModel(id=1, name="Bar1")
    bar2 = BarModel(id=2, name="Bar2")

    bar1.parent_id = bar2.id
    bar1.parent = bar2
    bar2.children.append(bar1)

    data = bar1.to_dict(nested=True)

    assert data == {
        "id": 1,
        "name": "Bar1",
        "upper_name": "BAR1",
        "parent_id": 2,
        "parent": {"id": 2, "name": "Bar2", "parent_id": None, "upper_name": "BAR2"},
        "children": [],
    }
