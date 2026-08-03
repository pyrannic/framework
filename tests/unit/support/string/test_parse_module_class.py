from pyrannic.support.string import parse_module_class


def test_parse_module_class():
    module = "foo.bar.my_module.MyClass"
    expected_module_name = "foo.bar.my_module"
    expected_class_name = "MyClass"

    module_name, class_name = parse_module_class(module)

    assert module_name == expected_module_name
    assert class_name == expected_class_name
