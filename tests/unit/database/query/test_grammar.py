import pytest

from pyrannic.database.query.expression import Expression
from pyrannic.database.query.grammar import Grammar


def test_wrap_asterisk():
    grammar = Grammar()

    assert grammar.wrap("*") == "*"


def test_wrap_single_segment():
    grammar = Grammar()

    assert grammar.wrap("users") == '"users"'


def test_wrap_multiple_segments():
    grammar = Grammar()

    assert grammar.wrap("users.id") == '"users"."id"'


def test_wrap_table_without_prefix():
    grammar = Grammar()

    assert grammar.wrap_table("users") == '"users"'


def test_wrap_table_with_prefix():
    grammar = Grammar()

    assert grammar.wrap_table("users", "app_") == '"app_users"'


def test_wrap_accepts_pre_quoted_single_segment():
    grammar = Grammar()

    assert grammar.wrap('"users"') == '"users"'


def test_wrap_accepts_pre_quoted_multiple_segments():
    grammar = Grammar()

    assert grammar.wrap('"users"."id"') == '"users"."id"'


def test_wrap_rejects_unbalanced_quotes():
    grammar = Grammar()

    with pytest.raises(ValueError, match="Invalid or insecure SQL identifier"):
        grammar.wrap('"users')


def test_wrap_rejects_embedded_quotes_inside_quoted_token():
    grammar = Grammar()

    with pytest.raises(ValueError, match="Invalid or insecure SQL identifier"):
        grammar.wrap('"na""me"')


def test_wrap_with_raw_expression():
    grammar = Grammar()
    expression = Expression("users.id")

    assert grammar.wrap(expression) == "users.id"


def test_columnize():
    grammar = Grammar()

    assert grammar.columnize("users.id", "users.name") == '"users"."id", "users"."name"'


def test_columnize_with_expressions():
    grammar = Grammar()
    expression1 = Expression("users.id")
    expression2 = Expression("users.name")

    assert grammar.columnize(expression1, expression2) == "users.id, users.name"


def test_quote_string_allows_valid_identifier():
    grammar = Grammar()

    assert grammar.quote_string("users.id") == "'users.id'"


def test_quote_string_rejects_invalid_identifier():
    grammar = Grammar()

    with pytest.raises(ValueError, match="Invalid or insecure SQL identifier"):
        grammar.wrap("users; DROP TABLE users")


def test_escape_none():
    grammar = Grammar()

    assert grammar.escape(None) == "null"


def test_escape_bool_values():
    grammar = Grammar()

    assert grammar.escape(True) == "1"
    assert grammar.escape(False) == "0"


def test_escape_numeric_values():
    grammar = Grammar()

    assert grammar.escape(42) == "42"
    assert grammar.escape(3.14) == "3.14"


def test_escape_string_value():
    grammar = Grammar()

    assert grammar.escape("users") == "'users'"


def test_escape_binary_uses_binary_escape_method():
    class BinaryGrammar(Grammar):
        def _escape_binary(self, value: str) -> str:
            return f"binary:{value}"

    grammar = BinaryGrammar()

    assert grammar.escape("0101", binary=True) == "binary:0101"


def test_escape_binary_rejects_non_string_values():
    grammar = Grammar()

    with pytest.raises(AssertionError):
        grammar.escape(1.5, binary=True)


def test_escape_binary_base_method_not_implemented_through_public_interface():
    grammar = Grammar()

    with pytest.raises(NotImplementedError):
        grammar.escape("0101", binary=True)
