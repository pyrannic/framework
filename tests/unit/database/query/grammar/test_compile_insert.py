from pyrannic.database import Grammar, QueryBuilder


def test_compile_insert_single_record():
    grammar = Grammar()
    query_builder = QueryBuilder(grammar)

    sql = grammar.compile_insert(
        query_builder.from_("users"),
        [{"id": 1, "name": "David Smith"}],
    )

    assert sql == 'INSERT INTO "users" ("id", "name") VALUES (%s, %s)'


def test_compile_insert_multiple_records():
    grammar = Grammar()
    query_builder = QueryBuilder(grammar)

    sql = grammar.compile_insert(
        query_builder.from_("users"),
        [
            {"id": 1, "name": "David Smith"},
            {"id": 2, "name": "Sam Smith"},
            {"id": 3, "name": "Rick Smith"},
            {"id": 4, "name": "Chris Smith"},
        ],
    )

    assert (
        sql
        == 'INSERT INTO "users" ("id", "name") VALUES (%s, %s), (%s, %s), (%s, %s), (%s, %s)'
    )
