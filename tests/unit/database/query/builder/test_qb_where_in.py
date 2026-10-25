from pyrannic.database import Grammar, QueryBuilder


def test_simple_where_in():
    grammar = Grammar()
    query_builder = QueryBuilder(grammar)

    query_builder.select("id").from_("users").where_in("id", [1, 2, 3])
    sql = query_builder.to_sql()

    assert sql == 'SELECT "id" FROM "users" WHERE "id" IN (%s, %s, %s)'
    assert query_builder.get_bindings() == [1, 2, 3]


def test_simple_where_not_in():
    grammar = Grammar()
    query_builder = QueryBuilder(grammar)

    query_builder.select("id").from_("users").where_not_in("id", [1, 2, 3])
    sql = query_builder.to_sql()

    assert sql == 'SELECT "id" FROM "users" WHERE "id" NOT IN (%s, %s, %s)'
    assert query_builder.get_bindings() == [1, 2, 3]


def test_or_where_in():
    grammar = Grammar()
    query_builder = QueryBuilder(grammar)

    query_builder.select("id").from_("users").where("id", 1).or_where_in(
        "id", [2, 3, 4]
    )
    sql = query_builder.to_sql()

    assert sql == 'SELECT "id" FROM "users" WHERE "id" = %s OR "id" IN (%s, %s, %s)'
    assert query_builder.get_bindings() == [1, 2, 3, 4]
