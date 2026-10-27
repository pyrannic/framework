import copy

from pyrannic.database import Grammar, QueryBuilder


def test_copy():
    grammar = Grammar()
    query_builder = QueryBuilder(grammar)
    query_builder.select("id").from_("users").where("id", 1)

    cloned_query_builder = copy.copy(query_builder)
    assert cloned_query_builder.to_sql() == query_builder.to_sql()
    assert cloned_query_builder.get_bindings() == query_builder.get_bindings()


def test_deepcopy():
    grammar = Grammar()
    query_builder = QueryBuilder(grammar)
    query_builder.select("id").from_("users").where("id", 1)

    cloned_query_builder = copy.deepcopy(query_builder)
    assert cloned_query_builder.to_sql() == query_builder.to_sql()
    assert cloned_query_builder.get_bindings() == query_builder.get_bindings()
