from pyrannic.database import Grammar


def test_wrap_with_aliases():
    grammar = Grammar()
    assert grammar.wrap("users as u") == '"users" AS "u"'
    assert grammar.wrap("users AS user") == '"users" AS "user"'
