from pyrannic.database import Grammar, QueryBuilder


def test_distinct():
    grammar = Grammar()
    query_builder = QueryBuilder(grammar)

    query_builder.select("id").distinct().from_("users").where_in("id", [1, 2, 3])
    sql = query_builder.to_sql()

    assert sql == 'SELECT DISTINCT "id" FROM "users" WHERE "id" IN (%s, %s, %s)'
    assert query_builder.get_bindings() == [1, 2, 3]


def test_distinct_columns():
    grammar = Grammar()
    query_builder = QueryBuilder(grammar)

    query_builder.select("id", "name").distinct("name").from_("users")
    assert query_builder.distinct_columns == ["name"]
