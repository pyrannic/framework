from pyrannic.database import Grammar, QueryBuilder


def test_join_sub():
    grammar = Grammar()
    query_builder = QueryBuilder(grammar)

    query_builder.from_("users").join_sub(
        QueryBuilder(grammar).select("id").from_("orders"),
        "sub",
        "users.id",
        "=",
        "sub.user_id",
    )

    sql = query_builder.to_sql()

    assert (
        sql
        == 'SELECT * FROM "users" INNER JOIN (SELECT "id" FROM "orders") as "sub" ON "users"."id" = "sub"."user_id"'
    )
