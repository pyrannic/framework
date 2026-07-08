import tests.unit.support.reflection.conftest as conftest
from pyrannic.support.reflection import get_class


def test_get_class__class_not_found():
    class_ = get_class(conftest, class_name="NonExistentClass")
    assert class_ is None


def test_get_class__module_not_found():
    class_ = get_class("non_existent_module", class_name="NonExistentClass")
    assert class_ is None


def test_get_class_without_args():
    class_ = get_class(conftest)
    assert class_ is conftest.Conftest


def test_get_class_with_class_name():
    class_ = get_class(conftest, class_name="FooClass")

    assert class_ is conftest.FooClass


def test_get_class_with_class_suffix():
    class_ = get_class(conftest, class_suffix="WithSuffix")

    assert class_ is conftest.ConftestWithSuffix


def test_get_class_without_args_using_string_module_name():
    class_ = get_class("conftest")
    assert class_ is not None
    assert "conftest.Conftest" in class_.__module__ + "." + class_.__name__


def test_get_class_with_class_name_using_string_module_name():
    class_ = get_class("conftest", class_name="FooClass")
    assert class_ is not None
    assert "conftest.FooClass" in class_.__module__ + "." + class_.__name__


def test_get_class_with_class_suffix_using_string_module_name():
    class_ = get_class("conftest", class_suffix="WithSuffix")
    assert class_ is not None
    assert "conftest.ConftestWithSuffix" in class_.__module__ + "." + class_.__name__
