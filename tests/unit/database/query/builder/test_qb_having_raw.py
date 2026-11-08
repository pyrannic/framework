from pyrannic.database import Grammar, QueryBuilder


def test_having_raw():
    grammar = Grammar()
    query_builder = QueryBuilder(grammar)

    query_builder.from_("users").group_by("user_id").having_raw(
        '"user_id" = %s', bindings=[10]
    )
    sql = query_builder.to_sql()

    assert sql == 'SELECT * FROM "users" GROUP BY "user_id" HAVING "user_id" = %s'
    assert query_builder.get_bindings() == [10]


def test_having_raw_with_multiple_conditions():
    grammar = Grammar()
    query_builder = QueryBuilder(grammar)

    query_builder.from_("users").group_by("user_id").having_raw(
        '"user_id" = %s', bindings=[10]
    ).having_raw('"age" > %s', bindings=[18])
    sql = query_builder.to_sql()

    assert (
        sql
        == 'SELECT * FROM "users" GROUP BY "user_id" HAVING "user_id" = %s AND "age" > %s'
    )
    assert query_builder.get_bindings() == [10, 18]


def test_or_having_raw():
    grammar = Grammar()
    query_builder = QueryBuilder(grammar)

    query_builder.from_("users").group_by("user_id").having_raw(
        '"user_id" = %s', bindings=[10]
    ).or_having_raw('"age" > %s', bindings=[18])
    sql = query_builder.to_sql()

    assert (
        sql
        == 'SELECT * FROM "users" GROUP BY "user_id" HAVING "user_id" = %s OR "age" > %s'
    )
    assert query_builder.get_bindings() == [10, 18]
