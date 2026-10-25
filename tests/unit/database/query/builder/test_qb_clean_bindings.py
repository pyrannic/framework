from typing import Any

from pyrannic.database import Grammar, QueryBuilder


def test_clean_bindings():
    grammar = Grammar()
    query_builder = QueryBuilder(grammar)

    bindings: list[Any] = [2, query_builder.raw("NOW()"), "David"]
    bindings = query_builder.clean_bindings(bindings)
    assert bindings == [2, "David"]
