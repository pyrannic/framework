from pyrannic.database import Grammar, QueryBuilder


def test_compile_delete_with_where():
    grammar = Grammar()
    query_builder = QueryBuilder(grammar)

    query_builder.from_("users").where("id", "=", 1)
    sql = grammar.compile_delete(query_builder)

    assert sql == 'DELETE FROM "users" WHERE "id" = %s'
    assert query_builder.get_bindings() == [1]


def test_compile_delete_without_where():
    grammar = Grammar()
    query_builder = QueryBuilder(grammar)

    query_builder.from_("users")
    sql = grammar.compile_delete(query_builder)

    assert sql == 'DELETE FROM "users"'


def test_compile_delete_with_join():
    grammar = Grammar()
    query_builder = QueryBuilder(grammar)

    query_builder.from_("users").join(
        "profiles", "users.id", "=", "profiles.user_id"
    ).where("id", "=", 1)
    sql = grammar.compile_delete(query_builder)

    assert (
        sql
        == 'DELETE FROM "users" INNER JOIN "profiles" ON "users"."id" = "profiles"."user_id" WHERE "id" = %s'
    )
    assert query_builder.get_bindings() == [1]


def test_compile_delete_with_join_and_alias():
    grammar = Grammar()
    query_builder = QueryBuilder(grammar)

    query_builder.from_("users", "u").join(
        "profiles as p", "u.id", "=", "p.user_id"
    ).where("id", "=", 1)
    sql = grammar.compile_delete(query_builder)

    assert (
        sql
        == 'DELETE "u" FROM "users" AS "u" INNER JOIN "profiles" AS "p" ON "u"."id" = "p"."user_id" WHERE "id" = %s'
    )
    assert query_builder.get_bindings() == [1]
