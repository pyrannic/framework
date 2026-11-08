from pyrannic.database import Grammar, QueryBuilder


def test_having_null():
    grammar = Grammar()
    query_builder = QueryBuilder(grammar)

    query_builder.from_("users").group_by("user_id").having_null("user_id")
    sql = query_builder.to_sql()

    assert sql == 'SELECT * FROM "users" GROUP BY "user_id" HAVING "user_id" IS NULL'
    assert query_builder.get_bindings() == []


def test_or_having_null():
    grammar = Grammar()
    query_builder = QueryBuilder(grammar)

    query_builder.from_("users").group_by("user_id").having_null(
        "user_id"
    ).or_having_null("name")
    sql = query_builder.to_sql()

    assert (
        sql
        == 'SELECT * FROM "users" GROUP BY "user_id" HAVING "user_id" IS NULL OR "name" IS NULL'
    )
    assert query_builder.get_bindings() == []


def test_having_not_null():
    grammar = Grammar()
    query_builder = QueryBuilder(grammar)

    query_builder.from_("users").group_by("user_id").having_not_null("user_id")
    sql = query_builder.to_sql()

    assert (
        sql == 'SELECT * FROM "users" GROUP BY "user_id" HAVING "user_id" IS NOT NULL'
    )
    assert query_builder.get_bindings() == []


def test_or_having_not_null():
    grammar = Grammar()
    query_builder = QueryBuilder(grammar)

    query_builder.from_("users").group_by("user_id").having_not_null(
        "user_id"
    ).or_having_not_null("name")
    sql = query_builder.to_sql()

    assert (
        sql
        == 'SELECT * FROM "users" GROUP BY "user_id" HAVING "user_id" IS NOT NULL OR "name" IS NOT NULL'
    )
    assert query_builder.get_bindings() == []
