from pyrannic.database import Grammar, QueryBuilder


def test_where_with_only_column():
    grammar = Grammar()
    query_builder = QueryBuilder(grammar)

    query_builder.select("*").from_("users").where("last_name", None)
    sql = query_builder.to_sql()
    raw_sql = query_builder.to_raw_sql()

    assert sql == 'SELECT * FROM "users" WHERE "last_name" IS %s'
    assert raw_sql == 'SELECT * FROM "users" WHERE "last_name" IS NULL'
    assert query_builder.get_bindings() == [None]


def test_where_comparing_column_to_subquery():
    grammar = Grammar()
    query_builder = QueryBuilder(grammar)

    query_builder.select("action_id").from_("actions").where_not_null(
        "action_id"
    ).where(
        "version_date_time",
        "=",
        QueryBuilder(grammar)
        .select("version_date_time")
        .from_("versions")
        .where("version_rank", 2),
    )
    sql = query_builder.to_sql()

    assert (
        sql
        == 'SELECT "action_id" FROM "actions" WHERE "action_id" IS NOT NULL AND "version_date_time" = (SELECT "version_date_time" FROM "versions" WHERE "version_rank" = %s)'
    )
    assert query_builder.get_bindings() == [2]
