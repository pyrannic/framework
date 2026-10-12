from pyrannic.database.query.clauses.order_by import OrderByClause, SortDirection
from pyrannic.database.query.expression import Expression


def test_equality():
    order_by_1 = OrderByClause("users.id", SortDirection.ASC)
    order_by_2 = OrderByClause("users.id", SortDirection.ASC)

    assert order_by_1 == order_by_2


def test_equality_with_raw_expression():
    expression = Expression("users.id ASC")

    order_by_1 = OrderByClause("users.id", SortDirection.ASC)
    order_by_2 = OrderByClause(expression)

    assert order_by_1 == order_by_2


def test_inequality():
    order_by_1 = OrderByClause("users.id", SortDirection.ASC)
    order_by_2 = OrderByClause("users.id", SortDirection.DESC)
    order_by_3 = OrderByClause("users.id", SortDirection.ASC)

    assert order_by_1 != order_by_2
    assert order_by_1 == order_by_3
    assert order_by_2 != order_by_3
    assert order_by_1 != "instance_other_type"


def test_repr():
    order_by = OrderByClause("users.id", SortDirection.ASC)
    expected = (
        f"OrderByClause(column='users.id', direction='{SortDirection.ASC.value}')"
    )
    assert repr(order_by) == expected


def test_repr_with_raw_expression():
    expression = Expression("users.id ASC")
    order_by = OrderByClause(expression)
    expected = f"OrderByClause(expression={expression!r})"
    assert repr(order_by) == expected
