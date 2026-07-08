import tests.unit.support.reflection.conftest as conftest
from pyrannic.support.reflection import get_attrs


def test_get_attrs__attrs_not_found():
    attrs = get_attrs([conftest], "non_existent_attr")
    assert len(attrs) == 0


def test_get_attrs__module_not_found():
    attrs = get_attrs(["non_existent_module"], "non_existent_attr")
    assert len(attrs) == 0


def test_get_attrs():
    attrs = get_attrs([conftest], "foo_attr")

    assert "foo_attr_value" in attrs


def test_get_attrs_with_default_value():
    attrs = get_attrs([conftest], "non_existent_attr", default="default_value")

    assert "default_value" in attrs


def test_get_attrs_using_string_module_name():
    attrs = get_attrs(["conftest"], "foo_attr")

    assert "foo_attr_value" in attrs


def test_get_attrs_with_default_value_using_string_module_name():
    attrs = get_attrs(["conftest"], "non_existent_attr", default="default_value")

    assert "default_value" in attrs
