import pytest

from pyrannic.contracts.database import (
    ExpressionInterface,
    JoinBuilderInterface,
    QueryBuilderInterface,
    SortDirection,
)
from pyrannic.database import Grammar, QueryBuilder


def test_select_using_default():
    grammar = Grammar()
    query_builder = QueryBuilder(grammar)

    assert query_builder.select().columns == ["*"]


def test_select_single_column():
    grammar = Grammar()
    query_builder = QueryBuilder(grammar)

    assert query_builder.select("foo").columns == ["foo"]


def test_select_multiple_columns():
    grammar = Grammar()
    query_builder = QueryBuilder(grammar)

    assert query_builder.select("foo", "bar").columns == ["foo", "bar"]


def test_select_reset_columns():
    grammar = Grammar()
    query_builder = QueryBuilder(grammar)

    assert query_builder.select("foo", "bar").columns == ["foo", "bar"]
    query_builder.select("baz")
    assert query_builder.columns == ["baz"]


def test_add_select():
    grammar = Grammar()
    query_builder = QueryBuilder(grammar)

    query_builder.select("foo").add_select("bar")
    assert query_builder.columns == ["foo", "bar"]


def test_add_select_multiple_columns():
    grammar = Grammar()
    query_builder = QueryBuilder(grammar)

    query_builder.select("foo").add_select("bar", "baz")
    assert query_builder.columns == ["foo", "bar", "baz"]


def test_add_select_with_no_additional_columns():
    grammar = Grammar()
    query_builder = QueryBuilder(grammar)

    query_builder.select("foo").add_select()
    assert query_builder.columns == ["foo"]


def test_add_select_avoid_repeating_columns():
    grammar = Grammar()
    query_builder = QueryBuilder(grammar)

    query_builder.select("foo").add_select("foo", "bar")
    assert query_builder.columns == ["foo", "bar"]


def test_select_raw():
    grammar = Grammar()
    query_builder = QueryBuilder(grammar)

    query_builder.select_raw("INFORMATION_SCHEMA.COLUMNS.ordinal_position").from_(
        "users"
    ).offset(5)
    sql = query_builder.to_sql()

    assert (
        sql
        == 'SELECT INFORMATION_SCHEMA.COLUMNS.ordinal_position FROM "users" OFFSET 5'
    )


def test_select_raw_with_bindings():
    grammar = Grammar()
    query_builder = QueryBuilder(grammar)

    query_builder.select_raw(
        "INFORMATION_SCHEMA.COLUMNS.ordinal_position = ?", "5"
    ).from_("users")
    sql = query_builder.to_sql()

    assert sql == 'SELECT INFORMATION_SCHEMA.COLUMNS.ordinal_position = ? FROM "users"'
    assert query_builder.get_bindings() == ["5"]


def test_distinct():
    grammar = Grammar()
    query_builder = QueryBuilder(grammar)

    assert not query_builder.is_distinct
    query_builder.distinct()
    assert query_builder.is_distinct


def test_from():
    grammar = Grammar()
    query_builder = QueryBuilder(grammar)

    assert query_builder.from_clause == ""
    query_builder.from_("users")
    assert query_builder.from_clause == "users"


def test_from_with_alias():
    grammar = Grammar()
    query_builder = QueryBuilder(grammar)

    assert query_builder.from_clause == ""
    query_builder.from_("users", as_="u")
    assert query_builder.from_clause == "users as u"


def test_where_simple():
    grammar = Grammar()
    query_builder = QueryBuilder(grammar)

    query_builder.where("foo", "bar")
    where_clause = query_builder.wheres[0]

    assert where_clause.column == "foo"
    assert where_clause.value == "bar"
    assert where_clause.operator == "="
    assert where_clause.boolean == "and"


def test_where_with_operator():
    grammar = Grammar()
    query_builder = QueryBuilder(grammar)

    query_builder.where("foo", "!=", "bar")
    where_clause = query_builder.wheres[0]

    assert where_clause.column == "foo"
    assert where_clause.value == "bar"
    assert where_clause.operator == "!="
    assert where_clause.boolean == "and"


def test_where_compare_with_none():
    grammar = Grammar()
    query_builder = QueryBuilder(grammar)

    query_builder.where("foo", None)
    where_clause = query_builder.wheres[0]

    assert where_clause.column == "foo"
    assert where_clause.value is None
    assert where_clause.operator == "="
    assert where_clause.boolean == "and"


def test_where_with_callable():
    grammar = Grammar()
    query_builder = QueryBuilder(grammar)

    def callback(qb: QueryBuilderInterface):
        qb.where("foo", "bar").where("baz", "qux")

    query_builder.where("id", 1).or_where(callback)
    where_clause = query_builder.wheres[1]

    assert where_clause.type == "nested"
    assert where_clause.boolean == "or"
    assert where_clause.query is not None


def test_or_where_simple():
    grammar = Grammar()
    query_builder = QueryBuilder(grammar)

    query_builder.where("foo", "baz").or_where("foo", "bar")
    where_clause = query_builder.wheres[1]

    assert where_clause.column == "foo"
    assert where_clause.value == "bar"
    assert where_clause.operator == "="
    assert where_clause.boolean == "or"


def test_or_where_simple_with_operator():
    grammar = Grammar()
    query_builder = QueryBuilder(grammar)

    query_builder.where("foo", "baz").or_where("foo", "!=", "bar")
    where_clause = query_builder.wheres[1]

    assert where_clause.column == "foo"
    assert where_clause.value == "bar"
    assert where_clause.operator == "!="
    assert where_clause.boolean == "or"


def test_group_by():
    grammar = Grammar()
    query_builder = QueryBuilder(grammar)

    query_builder.group_by("foo", "bar")
    groups = query_builder.groups

    assert "foo" in groups
    assert "bar" in groups


def test_group_by_raw():
    grammar = Grammar()
    query_builder = QueryBuilder(grammar)

    query_builder.group_by_raw("foo, bar")
    group = query_builder.groups[0]

    assert isinstance(group, ExpressionInterface)
    assert group.get_value(grammar) == "foo, bar"


def test_order_by():
    grammar = Grammar()
    query_builder = QueryBuilder(grammar)

    query_builder.order_by("foo", SortDirection.ASC)
    order_clause = query_builder.orders[0]

    assert order_clause.column == "foo"
    assert order_clause.direction == SortDirection.ASC


def test_order_by_desc():
    grammar = Grammar()
    query_builder = QueryBuilder(grammar)

    query_builder.order_by_desc("foo")
    order_clause = query_builder.orders[0]

    assert order_clause.column == "foo"
    assert order_clause.direction == SortDirection.DESC


def test_order_by_asc():
    grammar = Grammar()
    query_builder = QueryBuilder(grammar)

    query_builder.order_by_asc("foo")
    order_clause = query_builder.orders[0]

    assert order_clause.column == "foo"
    assert order_clause.direction == SortDirection.ASC


def test_order_by_raw():
    grammar = Grammar()
    query_builder = QueryBuilder(grammar)

    query_builder.order_by_raw("INFORMATION_SCHEMA.COLUMNS.ordinal_position ASC")
    order_clause = query_builder.orders[0]

    assert order_clause.is_raw
    assert order_clause.column is None
    assert order_clause.expression is not None
    assert (
        order_clause.expression.get_value(grammar)
        == "INFORMATION_SCHEMA.COLUMNS.ordinal_position ASC"
    )


def test_latest():
    grammar = Grammar()
    query_builder = QueryBuilder(grammar)

    query_builder.latest("created_at")
    order_clause = query_builder.orders[0]

    assert order_clause.column == "created_at"
    assert order_clause.direction == SortDirection.DESC


def test_latest_with_custom_column():
    grammar = Grammar()
    query_builder = QueryBuilder(grammar)

    query_builder.latest("updated_at")
    order_clause = query_builder.orders[0]

    assert order_clause.column == "updated_at"
    assert order_clause.direction == SortDirection.DESC


def test_oldest():
    grammar = Grammar()
    query_builder = QueryBuilder(grammar)

    query_builder.oldest("created_at")
    order_clause = query_builder.orders[0]

    assert order_clause.column == "created_at"
    assert order_clause.direction == SortDirection.ASC


def test_oldest_with_custom_column():
    grammar = Grammar()
    query_builder = QueryBuilder(grammar)

    query_builder.oldest("updated_at")
    order_clause = query_builder.orders[0]

    assert order_clause.column == "updated_at"
    assert order_clause.direction == SortDirection.ASC


def test_skip():
    grammar = Grammar()
    query_builder = QueryBuilder(grammar)

    query_builder.skip(5)
    assert query_builder.offset_count == 5


def test_offset():
    grammar = Grammar()
    query_builder = QueryBuilder(grammar)

    query_builder.offset(5)
    assert query_builder.offset_count == 5


def test_take():
    grammar = Grammar()
    query_builder = QueryBuilder(grammar)

    query_builder.take(5)
    assert query_builder.limit_count == 5


def test_limit():
    grammar = Grammar()
    query_builder = QueryBuilder(grammar)

    query_builder.limit(5)
    assert query_builder.limit_count == 5


def test_to_sql_with_simple_select():
    grammar = Grammar()
    query_builder = QueryBuilder(grammar)

    query_builder.select("id").from_("users")
    sql = query_builder.to_sql()

    assert sql == 'SELECT "id" FROM "users"'


def test_to_sql_with_simple_select_and_distinct():
    grammar = Grammar()
    query_builder = QueryBuilder(grammar)

    query_builder.select("id").distinct().from_("users")
    sql = query_builder.to_sql()

    assert sql == 'SELECT DISTINCT "id" FROM "users"'


def test_to_sql_with_simple_where():
    grammar = Grammar()
    query_builder = QueryBuilder(grammar)

    query_builder.select("id").from_("users").where("id", 1)
    sql = query_builder.to_sql()

    assert sql == 'SELECT "id" FROM "users" WHERE "id" = %s'
    assert query_builder.get_bindings() == [1]


def test_to_sql_with_simple_or_where():
    grammar = Grammar()
    query_builder = QueryBuilder(grammar)

    query_builder.select("id").from_("users").where("id", 1).or_where("name", "john")
    sql = query_builder.to_sql()

    assert sql == 'SELECT "id" FROM "users" WHERE "id" = %s OR "name" = %s'
    assert query_builder.get_bindings() == [1, "john"]


def test_to_sql_with_nested_where():
    grammar = Grammar()
    query_builder = QueryBuilder(grammar)

    query_builder.select("id").from_("users").where("id", 1).or_where(
        lambda qb: qb.where("foo", "bar").where("baz", "qux")
    )
    sql = query_builder.to_sql()

    assert (
        sql == 'SELECT "id" FROM "users" WHERE "id" = %s OR ("foo" = %s AND "baz" = %s)'
    )
    assert query_builder.get_bindings() == [1, "bar", "qux"]


def test_to_sql_with_empty_where_nested():
    grammar = Grammar()
    query_builder = QueryBuilder(grammar)

    query_builder.select("id").from_("users").where_nested(lambda qb: None)
    sql = query_builder.to_sql()

    assert sql == 'SELECT "id" FROM "users"'


def test_to_sql_with_where_column():
    grammar = Grammar()
    query_builder = QueryBuilder(grammar)

    query_builder.select("id").from_("users").where_column("id", "user_id")
    sql = query_builder.to_sql()

    assert sql == 'SELECT "id" FROM "users" WHERE "id" = "user_id"'


def test_to_sql_with_group_by():
    grammar = Grammar()
    query_builder = QueryBuilder(grammar)

    query_builder.select("id").from_("users").group_by("foo", "bar")
    sql = query_builder.to_sql()

    assert sql == 'SELECT "id" FROM "users" GROUP BY "foo", "bar"'


def test_to_sql_with_group_by_raw():
    grammar = Grammar()
    query_builder = QueryBuilder(grammar)

    query_builder.select("id").from_("users").group_by_raw("foo, bar")
    sql = query_builder.to_sql()

    assert sql == 'SELECT "id" FROM "users" GROUP BY foo, bar'


def test_to_sql_with_simple_select_join():
    grammar = Grammar()
    query_builder = QueryBuilder(grammar)

    query_builder.select("id").distinct().from_("users").join(
        "posts", "users.id", "=", "posts.user_id"
    )
    sql = query_builder.to_sql()

    assert (
        sql
        == 'SELECT DISTINCT "id" FROM "users" INNER JOIN "posts" ON "users"."id" = "posts"."user_id"'
    )


def test_to_sql_with_join_with_expression():
    grammar = Grammar()
    query_builder = QueryBuilder(grammar)

    def join_condition(builder: JoinBuilderInterface):
        builder.on(
            query_builder.raw(
                "UPPER(SUBSTR(INFORMATION_SCHEMA.COLUMNS.table_name, 4))"
            ),
            "=",
            query_builder.raw("UPPER(SUBSTR(config_table, 4))"),
        ).on(
            query_builder.raw("INFORMATION_SCHEMA.COLUMNS.column_name"),
            "=",
            query_builder.raw("config_table_column"),
        )

    query_builder.select("id").from_("users").join(
        query_builder.raw("INFORMATION_SCHEMA.COLUMNS"),
        join_condition,
    )
    sql = query_builder.to_sql()

    assert (
        sql == 'SELECT "id" '
        'FROM "users" '
        "INNER JOIN INFORMATION_SCHEMA.COLUMNS ON "
        "UPPER(SUBSTR(INFORMATION_SCHEMA.COLUMNS.table_name, 4)) = UPPER(SUBSTR(config_table, 4)) AND "
        "INFORMATION_SCHEMA.COLUMNS.column_name = config_table_column"
    )


def test_to_sql_with_simple_order_by():
    grammar = Grammar()
    query_builder = QueryBuilder(grammar)

    query_builder.select().from_("users").order_by("id", SortDirection.ASC)
    sql = query_builder.to_sql()

    assert sql == 'SELECT * FROM "users" ORDER BY "id" ASC'


def test_to_sql_with_simple_order_by_with_multiple_columns():
    grammar = Grammar()
    query_builder = QueryBuilder(grammar)

    query_builder.select().from_("users").order_by("id", SortDirection.DESC).order_by(
        "email", SortDirection.ASC
    )
    sql = query_builder.to_sql()

    assert sql == 'SELECT * FROM "users" ORDER BY "id" DESC, "email" ASC'


def test_to_sql_with_latest():
    grammar = Grammar()
    query_builder = QueryBuilder(grammar)

    query_builder.select().from_("users").latest()
    sql = query_builder.to_sql()

    assert sql == 'SELECT * FROM "users" ORDER BY "created_at" DESC'


def test_to_sql_with_oldest():
    grammar = Grammar()
    query_builder = QueryBuilder(grammar)

    query_builder.select().from_("users").oldest()
    sql = query_builder.to_sql()

    assert sql == 'SELECT * FROM "users" ORDER BY "created_at" ASC'


def test_to_sql_with_order_by_raw():
    grammar = Grammar()
    query_builder = QueryBuilder(grammar)

    query_builder.select().from_("users").order_by_raw(
        "INFORMATION_SCHEMA.COLUMNS.ordinal_position ASC"
    ).offset(5)
    sql = query_builder.to_sql()

    assert (
        sql
        == 'SELECT * FROM "users" ORDER BY INFORMATION_SCHEMA.COLUMNS.ordinal_position ASC OFFSET 5'
    )


def test_to_raw_sql_with_simple_where_clause():
    grammar = Grammar()

    query_builder = QueryBuilder(grammar)
    query_builder.select("id").from_("users").where("id", 1)
    sql = query_builder.to_raw_sql()

    assert sql == 'SELECT "id" FROM "users" WHERE "id" = 1'

    query_builder = QueryBuilder(grammar)
    query_builder.select("id").from_("users").where("email", "test@example.com")
    sql = query_builder.to_raw_sql()

    assert sql == 'SELECT "id" FROM "users" WHERE "email" = \'test@example.com\''

    query_builder = QueryBuilder(grammar)
    query_builder.select("id").from_("users").where("admin", True)
    sql = query_builder.to_raw_sql()

    assert sql == 'SELECT "id" FROM "users" WHERE "admin" = 1'


def test_to_sql_with_limit():
    grammar = Grammar()
    query_builder = QueryBuilder(grammar)

    query_builder.select("id").distinct().from_("users").limit(5)
    sql = query_builder.to_sql()

    assert sql == 'SELECT DISTINCT "id" FROM "users" LIMIT 5'


def test_to_sql_with_offset():
    grammar = Grammar()
    query_builder = QueryBuilder(grammar)

    query_builder.select("id").distinct().from_("users").offset(5)
    sql = query_builder.to_sql()

    assert sql == 'SELECT DISTINCT "id" FROM "users" OFFSET 5'


def test_add_binding_raises_invalid_type():
    grammar = Grammar()
    query_builder = QueryBuilder(grammar)

    with pytest.raises(ValueError) as exc_info:
        query_builder.add_binding(1, type="invalid")

    error = str(exc_info.value)
    assert "Invalid binding type: 'invalid'" in error
