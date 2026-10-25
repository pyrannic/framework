from typing import Any

from pyrannic.database import Grammar


def test_prepare_bindings_for_update():
    grammar = Grammar()
    bindings: dict[str, list[Any]] = {
        "with": [],
        "select": [],
        "from": [],
        "join": [],
        "where": [20],
        "group_by": ["id"],
        "having": [],
        "order_by": [],
        "union": [],
        "unionOrder": [],
    }
    values: dict[str, Any] = {"name": "John", "age": 30}
    prepared = grammar.prepare_bindings_for_update(bindings, values)
    assert prepared == ["John", 30, 20, "id"]
