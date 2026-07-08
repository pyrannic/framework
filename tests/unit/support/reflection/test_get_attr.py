import tests.unit.support.reflection.conftest as conftest
from pyrannic.support.reflection import get_attr


def test_get_attr__attr_not_found():
    attr = get_attr(conftest, "non_existent_attr")
    assert attr is None


def test_get_attr__module_not_found():
    attr = get_attr("non_existent_module", "non_existent_attr")
    assert attr is None


def test_get_attr():
    attr = get_attr(conftest, "foo_attr")

    assert attr == "foo_attr_value"


def test_get_attr_with_default_value():
    attr = get_attr(conftest, "non_existent_attr", default="default_value")

    assert attr == "default_value"


def test_get_attr_using_string_module_name():
    attr = get_attr("conftest", "foo_attr")

    assert attr == "foo_attr_value"


def test_get_attr_with_default_value_using_string_module_name():
    attr = get_attr("conftest", "non_existent_attr", default="default_value")

    assert attr == "default_value"
