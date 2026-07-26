from tests.unit.orm.sqlalchemy.utils import BarModel


def test_properties():
    assert BarModel.properties == ["upper_name"]


def test_columns():
    assert BarModel.columns == ["id", "name", "parent_id"]


def test_primary_keys_full():
    assert BarModel.primary_keys_full[0].key == "id"


def test_primary_keys():
    assert BarModel.primary_keys == ["id"]


def test_relations():
    assert BarModel.relations == ["parent", "children"]


def test_settable_relations():
    assert BarModel.settable_relations == ["parent", "children"]


def test_hybrid_properties():
    assert BarModel.hybrid_properties == ["slug"]


# TODO: Add hybrid methods to BarModel
def test_hybrid_methods_full():
    assert BarModel.hybrid_methods_full == {}


# TODO: Add hybrid methods to BarModel
def test_hybrid_methods():
    assert BarModel.hybrid_methods == []
