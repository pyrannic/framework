import pytest

from pyrannic.database import Grammar, QueryBuilder


def test_compile_joins_with_join_lateral():
    grammar = Grammar()
    query_builder = QueryBuilder(grammar)

    query_builder.select("id").from_("users").join_lateral(
        lambda q: q.from_("profiles").where("users.id", "=", "profiles.user_id"),
        as_="profiles",
    )

    with pytest.raises(NotImplementedError) as exc_info:
        grammar.compile_select(query_builder)

    error = str(exc_info.value)
    assert "This database engine does not support lateral joins" in error
