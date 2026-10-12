from pyrannic.database.query.clauses.where import WhereClause


def test_equality():
    where_1 = WhereClause("users.id", "=", 42)
    where_2 = WhereClause("users.id", "=", 42)

    assert where_1 == where_2


def test_inequality():
    where_1 = WhereClause("users.id", "=", 42)
    where_2 = WhereClause("users.id", "!=", 42)
    where_3 = WhereClause("users.id", ">", 42)

    assert where_1 != where_2
    assert where_1 != where_3
    assert where_2 != where_3
    assert where_1 != "instance_other_type"


def test_repr():
    where = WhereClause("users.id", "=", 42)
    expected = "WhereClause(column='users.id', operator='=', value=42, boolean='and', type='basic')"
    assert repr(where) == expected
