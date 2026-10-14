from pyrannic.database.query.builder import QueryBuilder
from pyrannic.database.query.grammar import Grammar
from pyrannic.database.query.join_builder import JoinBuilder


def test_parent_grammar():
    grammar = Grammar()
    query_builder = QueryBuilder(grammar)
    join_builder = JoinBuilder(query_builder, "inner", "users")

    assert join_builder.parent_grammar == grammar
    assert join_builder.parent_grammar == query_builder.grammar


def test_join_builder_type_and_table():
    grammar = Grammar()
    query_builder = QueryBuilder(grammar)
    join_builder = JoinBuilder(query_builder, "inner", "users")

    assert join_builder.type == "inner"
    assert join_builder.table == "users"


def test_join_on():
    grammar = Grammar()
    query_builder = QueryBuilder(grammar)
    join_builder = JoinBuilder(query_builder, "inner", "users")

    join_builder.on("users.id", "=", "posts.user_id")
    sql = join_builder.to_sql()

    assert sql == 'ON "users"."id" = "posts"."user_id"'


def test_join_on_without_operator():
    grammar = Grammar()
    query_builder = QueryBuilder(grammar)
    join_builder = JoinBuilder(query_builder, "inner", "users")

    join_builder.on("users.id", "posts.user_id")
    sql = join_builder.to_sql()

    assert sql == 'ON "users"."id" = "posts"."user_id"'


def test_join_with_multiple_on():
    grammar = Grammar()
    query_builder = QueryBuilder(grammar)
    join_builder = JoinBuilder(query_builder, "inner", "users")

    join_builder.on("contacts.user_id", "=", "users.id").on(
        "contacts.info_id", "=", "info.id"
    )
    sql = join_builder.to_sql()

    assert (
        sql
        == 'ON "contacts"."user_id" = "users"."id" AND "contacts"."info_id" = "info"."id"'
    )


def test_join_or_on():
    grammar = Grammar()
    query_builder = QueryBuilder(grammar)
    join_builder = JoinBuilder(query_builder, "inner", "users")

    join_builder.on("contacts.user_id", "=", "users.id").or_on(
        "contacts.info_id", "=", "info.id"
    )
    sql = join_builder.to_sql()

    assert (
        sql
        == 'ON "contacts"."user_id" = "users"."id" OR "contacts"."info_id" = "info"."id"'
    )


def test_join_or_on_without_operator():
    grammar = Grammar()
    query_builder = QueryBuilder(grammar)
    join_builder = JoinBuilder(query_builder, "inner", "users")

    join_builder.or_on("contacts.user_id", "users.id")
    sql = join_builder.to_sql()

    assert sql == 'ON "contacts"."user_id" = "users"."id"'


def test_join_or_on_with_expression():
    grammar = Grammar()
    query_builder = QueryBuilder(grammar)
    join_builder = JoinBuilder(query_builder, "inner", "users")

    join_builder.or_on(join_builder.raw("users.id"), join_builder.raw("posts.user_id"))
    sql = join_builder.to_sql()

    assert sql == "ON users.id = posts.user_id"
