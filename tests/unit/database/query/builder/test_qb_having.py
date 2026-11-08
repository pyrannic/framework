from pyrannic.database import Grammar, QueryBuilder


def test_simple_having_with_default_operator():
    grammar = Grammar()
    query_builder = QueryBuilder(grammar)

    query_builder.from_("users").group_by("user_id").having("user_id", 10)
    sql = query_builder.to_sql()

    assert sql == 'SELECT * FROM "users" GROUP BY "user_id" HAVING "user_id" = %s'
    assert query_builder.get_bindings() == [10]


def test_simple_having_with_default_operator_and_no_value():
    grammar = Grammar()
    query_builder = QueryBuilder(grammar)

    query_builder.from_("users").group_by("user_id").having("user_id")
    sql = query_builder.to_sql()

    assert sql == 'SELECT * FROM "users" GROUP BY "user_id" HAVING "user_id" IS NULL'


def test_simple_having_with_operator():
    grammar = Grammar()
    query_builder = QueryBuilder(grammar)

    query_builder.from_("users").group_by("user_id").having("user_id", ">", 10)
    sql = query_builder.to_sql()

    assert sql == 'SELECT * FROM "users" GROUP BY "user_id" HAVING "user_id" > %s'
    assert query_builder.get_bindings() == [10]
