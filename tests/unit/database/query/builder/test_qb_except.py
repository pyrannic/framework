from pyrannic.database import Grammar, QueryBuilder


def test_except():
    grammar = Grammar()
    query_builder = QueryBuilder(grammar)

    query_builder.select("action_id").from_("latest_actions").except_(
        QueryBuilder(grammar).select("action_id").from_("previous_actions")
    )
    sql = query_builder.to_sql()

    assert (
        sql
        == '(SELECT "action_id" FROM "latest_actions") EXCEPT (SELECT "action_id" FROM "previous_actions")'
    )
