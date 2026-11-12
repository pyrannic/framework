from pyrannic.database import Grammar, QueryBuilder


def test_cross_join_using_join_method():
    grammar = Grammar()
    query_builder = QueryBuilder(grammar)

    query_builder.from_("users").join(
        "orders",
        "users.id",
        "orders.user_id",
        type="cross",
    )

    sql = query_builder.to_sql()

    assert (
        sql
        == 'SELECT * FROM "users" CROSS JOIN "orders" ON "users"."id" = "orders"."user_id"'
    )


def test_cross_join_only_with_table():
    grammar = Grammar()
    query_builder = QueryBuilder(grammar)

    query_builder.from_("users").cross_join("orders")

    sql = query_builder.to_sql()

    assert sql == 'SELECT * FROM "users" CROSS JOIN "orders"'


def test_cross_join():
    grammar = Grammar()
    query_builder = QueryBuilder(grammar)

    query_builder.from_("users").cross_join("orders", "users.id", "orders.user_id")

    sql = query_builder.to_sql()

    assert (
        sql
        == 'SELECT * FROM "users" CROSS JOIN "orders" ON "users"."id" = "orders"."user_id"'
    )
