from tests.unit.orm.utils import FooModel, FooEntity, FooSchema, FooTable


def test_tablename():
    assert FooModel.tablename() == "foos"
    assert FooEntity.tablename() == "foos"
    assert FooSchema.tablename() == "foos"
    assert FooTable.tablename() == "foos"
