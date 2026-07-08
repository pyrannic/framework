import tests.unit.support.reflection.conftest as conftest
from pyrannic.support.reflection import get_classes


def test_get_classes__classes_not_found():
    classes = get_classes([conftest], class_name="NonExistentClass")
    assert classes == []


def test_get_classes__modules_not_found():
    classes = get_classes(["non_existent_module"], class_name="NonExistentClass")
    assert classes == []


def test_get_classes_without_args():
    classes = get_classes([conftest])
    assert classes == [conftest.Conftest]


def test_get_classes_with_class_name():
    classes = get_classes([conftest], class_name="FooClass")
    assert classes == [conftest.FooClass]


def test_get_classes_with_class_suffix():
    classes = get_classes([conftest], class_suffix="WithSuffix")
    assert classes == [conftest.ConftestWithSuffix]


def test_get_classes_without_args_using_string_module_name():
    classes = get_classes(["conftest"])
    assert "conftest.Conftest" in classes[0].__module__ + "." + classes[0].__name__


def test_get_classes_with_class_name_using_string_module_name():
    classes = get_classes(["conftest"], class_name="FooClass")
    assert "conftest.FooClass" in classes[0].__module__ + "." + classes[0].__name__


def test_get_classes_with_class_suffix_using_string_module_name():
    classes = get_classes(["conftest"], class_suffix="WithSuffix")
    assert (
        "conftest.ConftestWithSuffix"
        in classes[0].__module__ + "." + classes[0].__name__
    )
