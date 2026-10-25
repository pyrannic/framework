from pyrannic.database import Grammar, QueryBuilder


def test_clone():
    grammar = Grammar()
    query_builder = QueryBuilder(grammar)
    query_builder.select("id").from_("users").where("id", 1)

    cloned_query_builder = query_builder.clone()
    assert cloned_query_builder.to_sql() == query_builder.to_sql()
    assert cloned_query_builder.get_bindings() == query_builder.get_bindings()


def test_clone_independence():
    grammar = Grammar()
    query_builder = QueryBuilder(grammar)
    query_builder.select("id").from_("users").where("id", 1)

    cloned_query_builder = query_builder.clone()
    cloned_query_builder.where("id", 2)

    assert query_builder.to_sql() != cloned_query_builder.to_sql()
    assert query_builder.get_bindings() != cloned_query_builder.get_bindings()


def test_clone_with_raw_bindings():
    grammar = Grammar()
    query_builder = QueryBuilder(grammar)
    query_builder.select("id").from_("users").where("id", query_builder.raw("NOW()"))

    cloned_query_builder = query_builder.clone()
    assert cloned_query_builder.to_sql() == query_builder.to_sql()
    assert cloned_query_builder.get_bindings() == query_builder.get_bindings()


def test_clone_without():
    grammar = Grammar()
    query_builder = QueryBuilder(grammar)
    query_builder.select("id").from_("users")

    cloned_query_builder = query_builder.clone_without("from")

    assert query_builder.to_sql() == 'SELECT "id" FROM "users"'
    assert cloned_query_builder.to_sql() == 'SELECT "id"'
