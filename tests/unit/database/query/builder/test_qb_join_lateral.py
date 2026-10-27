import pytest

from pyrannic.database import Grammar, QueryBuilder


def test_left_join_lateral():
    grammar = Grammar()
    query_builder = QueryBuilder(grammar)

    query_builder.from_("users").left_join_lateral(
        QueryBuilder(grammar).select("id").from_("orders"), as_="sub"
    )

    with pytest.raises(NotImplementedError) as exc_info:
        query_builder.to_sql()

    error = str(exc_info.value)
    assert "This database engine does not support lateral joins" in error
