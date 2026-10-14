from pyrannic.database.query.expression import Expression


def test_expression_creation():
    expr = Expression("order by users.name")
    assert expr.get_value() == "order by users.name"

    expr = Expression(100)
    assert expr.get_value() == 100


def test_expression_equality():
    expr1 = Expression("order by users.name")
    expr2 = Expression("order by users.name")
    expr3 = Expression("order by users.id")

    assert expr1 == expr2
    assert expr1 != expr3
    assert expr3 == "order by users.id"
    assert expr3 != ["order by users.id"]

    expr4 = Expression(100)
    assert expr4 == 100
    assert expr4 != 200

    expr5 = Expression("100")
    assert expr5 == "100"
    assert expr5 != 100
