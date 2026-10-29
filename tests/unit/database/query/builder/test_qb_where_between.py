from pyrannic.database import Grammar, QueryBuilder


def test_where_between():
    grammar = Grammar()
    query_builder = QueryBuilder(grammar)

    query_builder.select("id").from_("users").where_between("id", [1, 10])
    sql = query_builder.to_sql()

    assert sql == 'SELECT "id" FROM "users" WHERE "id" BETWEEN %s AND %s'
    assert query_builder.get_bindings() == [1, 10]


def test_where_between_with_more_than_two_values():
    grammar = Grammar()
    query_builder = QueryBuilder(grammar)

    query_builder.select("id").from_("users").where_between("id", [1, 10, 20])
    sql = query_builder.to_sql()

    assert sql == 'SELECT "id" FROM "users" WHERE "id" BETWEEN %s AND %s'
    assert query_builder.get_bindings() == [1, 20]


def test_where_between_with_one_value():
    grammar = Grammar()
    query_builder = QueryBuilder(grammar)

    query_builder.select("id").from_("users").where_between("id", [1])
    sql = query_builder.to_sql()

    assert sql == 'SELECT "id" FROM "users" WHERE "id" BETWEEN %s AND %s'
    assert query_builder.get_bindings() == [1, 1]


def test_where_between_with_callable():
    grammar = Grammar()
    query_builder = QueryBuilder(grammar)

    query_builder.select("id").from_("users").where_between(
        lambda q: (
            q
            .from_("orders")
            .where_column("orders.user_id", "users.id")
            .set_aggregate("sum", "orders.total_amount")
        ),
        [1000, 5000],
    )
    sql = query_builder.to_sql()

    assert (
        sql
        == 'SELECT "id" FROM "users" WHERE (SELECT SUM("orders"."total_amount") AS "aggregate" FROM "orders" WHERE "orders"."user_id" = "users"."id") BETWEEN %s AND %s'
    )
    assert query_builder.get_bindings() == [1000, 5000]
