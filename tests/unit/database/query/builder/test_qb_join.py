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


def test_left_join_with_callable():
    grammar = Grammar()
    query_builder = QueryBuilder(grammar)

    query_builder.from_("users").left_join(
        "teams",
        lambda q: q.on("users.id", "teams.user_id").on(
            "teams.country_id", "users.country_id"
        ),
    )

    sql = query_builder.to_sql()

    assert (
        sql
        == 'SELECT * FROM "users" LEFT JOIN "teams" ON "users"."id" = "teams"."user_id" AND "teams"."country_id" = "users"."country_id"'
    )
