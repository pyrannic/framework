from typing import Any

from pyrannic.database import Grammar


def test_prepare_bindings_for_delete():
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
    prepared = grammar.prepare_bindings_for_delete(bindings)
    assert prepared == [20, "id"]
