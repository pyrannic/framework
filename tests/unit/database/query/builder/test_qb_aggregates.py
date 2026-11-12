from pyrannic.database import Grammar, QueryBuilder


def test_counts_with_excepts():
    grammar = Grammar()
    latest_actions = QueryBuilder(grammar).select("action_id").from_("latest_actions")
    previous_actions = (
        QueryBuilder(grammar).select("action_id").from_("previous_actions")
    )

    added = (
        QueryBuilder(grammar)
        .set_aggregate("count")
        .from_(latest_actions.clone().except_(previous_actions), as_="added")
    )

    removed = (
        QueryBuilder(grammar)
        .set_aggregate("count")
        .from_(previous_actions.clone().except_(latest_actions), as_="removed")
    )

    query_builder = (
        QueryBuilder(grammar)
        .select_subquery(added, "additions")
        .select_subquery(removed, "deletions")
    )
    sql = query_builder.to_sql()

    assert (
        sql
        == 'SELECT (SELECT COUNT(*) AS "aggregate" FROM ((SELECT "action_id" FROM "latest_actions") EXCEPT (SELECT "action_id" FROM "previous_actions")) AS "added") AS "additions", (SELECT COUNT(*) AS "aggregate" FROM ((SELECT "action_id" FROM "previous_actions") EXCEPT (SELECT "action_id" FROM "latest_actions")) AS "removed") AS "deletions"'
    )
