from pyrannic.database import Grammar, QueryBuilder


def test_left_join():
    grammar = Grammar()
    query_builder = QueryBuilder(grammar)

    query_builder.from_("users").left_join(
        "orders",
        "users.id",
        "=",
        "orders.user_id",
    )

    sql = query_builder.to_sql()

    assert (
        sql
        == 'SELECT * FROM "users" LEFT JOIN "orders" ON "users"."id" = "orders"."user_id"'
    )


def test_left_join_without_operator():
    grammar = Grammar()
    query_builder = QueryBuilder(grammar)

    query_builder.from_("users").left_join(
        "orders",
        "users.id",
        "orders.user_id",
    )

    sql = query_builder.to_sql()

    assert (
        sql
        == 'SELECT * FROM "users" LEFT JOIN "orders" ON "users"."id" = "orders"."user_id"'
    )
