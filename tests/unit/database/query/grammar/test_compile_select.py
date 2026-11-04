from pyrannic.database import Grammar, QueryBuilder


def test_compile_select_with_alias():
    grammar = Grammar()
    query_builder = QueryBuilder(grammar)

    query_builder.select("id", "title", "created_at as published_at").from_("posts")
    sql = grammar.compile_select(query_builder)

    assert sql == 'SELECT "id", "title", "created_at" AS "published_at" FROM "posts"'


def test_compile_select_with_alias_in_from():
    grammar = Grammar()
    query_builder = QueryBuilder(grammar)

    query_builder.from_("users", "u").where("id", "=", 1)
    sql = grammar.compile_select(query_builder)

    assert sql == 'SELECT * FROM "users" AS "u" WHERE "id" = %s'
    assert query_builder.get_bindings() == [1]


def test_compile_select_with_expression_in_from():
    grammar = Grammar()
    query_builder = QueryBuilder(grammar)

    query_builder.from_(query_builder.raw("users as u")).where("id", "=", 1)
    sql = grammar.compile_select(query_builder)

    assert sql == 'SELECT * FROM users as u WHERE "id" = %s'
    assert query_builder.get_bindings() == [1]


def test_compile_select_with_subquery_in_from():
    grammar = Grammar()
    query_builder = QueryBuilder(grammar)

    subquery = QueryBuilder(grammar).from_("users").where("status", "active")
    query_builder.from_(subquery, "u").where("id", "=", 1)
    sql = grammar.compile_select(query_builder)

    assert (
        sql
        == 'SELECT * FROM (SELECT * FROM "users" WHERE "status" = %s) AS "u" WHERE "id" = %s'
    )
    assert query_builder.get_bindings() == ["active", 1]
