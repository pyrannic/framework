from unittest.mock import Mock

import pytest

from pyrannic.contracts.database.schema import SchemaInterface
from tests.unit.database.utils import FooTable


def test_set_schema():
    schema: Mock = Mock(spec=SchemaInterface)

    migration: FooTable = FooTable()
    migration.set_schema(schema)

    assert migration.schema == schema


@pytest.mark.asyncio
async def test_up_and_down_methods():
    schema: Mock = Mock(spec=SchemaInterface)

    migration: FooTable = FooTable()
    migration.set_schema(schema)

    await migration.up()
    schema.create.assert_called_once_with("foo_table")

    await migration.down()
    schema.drop.assert_called_once_with("foo_table")
