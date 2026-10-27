from pyrannic.database import Grammar, QueryBuilder


def test_compile_update_single_value():
    grammar = Grammar()
    query_builder = QueryBuilder(grammar)

    query_builder.from_("users").where("id", 1)
    sql = grammar.compile_update(query_builder, {"name": "David Smith"})

    assert sql == 'UPDATE "users" SET "name" = %s WHERE "id" = %s'
    assert query_builder.get_bindings() == [1]


def test_compile_update_multiple_values():
    grammar = Grammar()
    query_builder = QueryBuilder(grammar)

    query_builder.from_("users").where("status", "active")
    sql = grammar.compile_update(
        query_builder, {"status": "inactive", "updated_at": "2024-06-10"}
    )

    assert (
        sql == 'UPDATE "users" SET "status" = %s, "updated_at" = %s WHERE "status" = %s'
    )
    assert query_builder.get_bindings() == ["active"]


def test_update_with_join():
    grammar = Grammar()
    query_builder = QueryBuilder(grammar)

    query_builder.from_("users").join(
        "profiles", "users.id", "=", "profiles.user_id"
    ).where("users.id", 1)
    sql = grammar.compile_update(query_builder, {"users.name": "David Smith"})

    assert (
        sql
        == 'UPDATE "users" INNER JOIN "profiles" ON "users"."id" = "profiles"."user_id" SET "users"."name" = %s WHERE "users"."id" = %s'
    )
    assert query_builder.get_bindings() == [1]
