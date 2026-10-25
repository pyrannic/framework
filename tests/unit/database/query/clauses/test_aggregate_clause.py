from pyrannic.database.query.clauses.aggregate import AggregateClause
from pyrannic.database.query.expression import Expression


def test_equality():
    aggregate_1 = AggregateClause("COUNT", ["users.id"])
    aggregate_2 = AggregateClause("COUNT", ["users.id"])

    assert aggregate_1 == aggregate_2


def test_equality_with_raw_expression():
    expression = Expression("users.id")

    aggregate_1 = AggregateClause("COUNT", ["users.id"])
    aggregate_2 = AggregateClause("COUNT", [expression])

    assert aggregate_1 == aggregate_2


def test_inequality():
    aggregate_1 = AggregateClause("COUNT", ["users.id"])
    aggregate_2 = AggregateClause("SUM", ["users.id"])
    aggregate_3 = AggregateClause("COUNT", ["users.id"])

    assert aggregate_1 != aggregate_2
    assert aggregate_1 == aggregate_3
    assert aggregate_2 != aggregate_3
    assert aggregate_1 != "instance_other_type"


def test_repr():
    aggregate = AggregateClause("COUNT", ["users.id"])
    expected = "AggregateClause(function='COUNT', columns=['users.id'])"
    assert repr(aggregate) == expected


def test_repr_with_raw_expression():
    expression = Expression("users.id")
    aggregate = AggregateClause("COUNT", [expression])
    expected = f"AggregateClause(function='COUNT', columns=[{expression!r}])"
    assert repr(aggregate) == expected
