from pyrannic.database import Grammar, QueryBuilder


def test_with_query_using_builder():
    grammar = Grammar()
    query_builder = QueryBuilder(grammar)

    query_builder.with_query(
        "cte_name",
        QueryBuilder(grammar).select("id").from_("users"),
    ).select("id").from_("cte_name")
    sql = query_builder.to_sql()

    assert (
        sql
        == 'WITH "cte_name" AS (SELECT "id" FROM "users") SELECT "id" FROM "cte_name"'
    )


def test_with_query_using_callback():
    grammar = Grammar()
    query_builder = QueryBuilder(grammar)

    query_builder.with_query(
        "cte_name", lambda q: q.select("id").from_("users")
    ).select("id").from_("cte_name")
    sql = query_builder.to_sql()

    assert (
        sql
        == 'WITH "cte_name" AS (SELECT "id" FROM "users") SELECT "id" FROM "cte_name"'
    )


def test_with_query_with_bindings():
    grammar = Grammar()
    query_builder = QueryBuilder(grammar)

    query_builder.with_query(
        "cte_name",
        QueryBuilder(grammar).select("id").from_("users").where("id", 1),
    ).select("id").from_("cte_name").where("name", "ilike", "%David%")
    sql = query_builder.to_sql()

    assert (
        sql
        == 'WITH "cte_name" AS (SELECT "id" FROM "users" WHERE "id" = %s) SELECT "id" FROM "cte_name" WHERE "name" ILIKE %s'
    )

    assert query_builder.get_bindings() == [1, "%David%"]
