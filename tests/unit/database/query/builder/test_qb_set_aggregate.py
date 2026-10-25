from pyrannic.database import Grammar, QueryBuilder


def test_set_aggregate():
    grammar = Grammar()
    query_builder = QueryBuilder(grammar)

    query_builder.set_aggregate("count", "id").from_("users")
    sql = query_builder.to_sql()

    assert sql == 'SELECT COUNT("id") AS "aggregate" FROM "users"'
