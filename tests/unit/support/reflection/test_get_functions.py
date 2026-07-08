import tests.unit.support.reflection.conftest as conftest

from pyrannic.support.reflection import get_functions


def test_get_functions_without_predicate():
    """Test the get_functions function without a predicate."""

    functions = get_functions(conftest)

    assert len(functions) == 3
    assert any(name == "foo_function" for name, _ in functions)
    assert any(name == "bar_function" for name, _ in functions)
    assert any(name == "baz_function" for name, _ in functions)


def test_get_functions_with_predicate():
    """Test the get_functions function with a predicate."""

    functions = get_functions(
        conftest,
        lambda name: name.startswith("foo"),
    )

    assert len(functions) == 1
    assert any(name == "foo_function" for name, _ in functions)
