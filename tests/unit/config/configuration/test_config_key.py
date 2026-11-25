from tests.unit.config.configuration.foo import Foo
from tests.unit.config.configuration.foo_config import FooBarConfig, FooConfig


def test_config_key(foo: Foo):
    assert foo.config_key == "foo"


def test_config_key_with_config_in_class_name(foo_config: FooConfig):
    assert foo_config.config_key == "foo"


def test_config_key_camel_case(foo_bar_config: FooBarConfig):
    assert foo_bar_config.config_key == "foo_bar"
