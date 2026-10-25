from pyrannic.database import Grammar, QueryBuilder


def test_compile_exists_with_simple_query():
    grammar = Grammar()
    query_builder = QueryBuilder(grammar)

    query_builder.select("id").from_("users")
    sql = grammar.compile_exists(query_builder)

    assert sql == 'SELECT exists(SELECT "id" FROM "users") AS "exists"'
