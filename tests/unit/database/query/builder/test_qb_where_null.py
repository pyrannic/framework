from pyrannic.database import Grammar, QueryBuilder


def test_simple_where_null():
    grammar = Grammar()
    query_builder = QueryBuilder(grammar)

    query_builder.select("id").from_("users").where_null("deleted_at")
    sql = query_builder.to_sql()

    assert sql == 'SELECT "id" FROM "users" WHERE "deleted_at" IS NULL'


def test_simple_where_not_null():
    grammar = Grammar()
    query_builder = QueryBuilder(grammar)

    query_builder.select("id").from_("users").where_not_null("deleted_at")
    sql = query_builder.to_sql()

    assert sql == 'SELECT "id" FROM "users" WHERE "deleted_at" IS NOT NULL'
