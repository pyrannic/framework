from tests.unit.config.configuration.foo import Foo
from tests.unit.config.configuration.foo_config import FooConfig


def test_config_key(foo: Foo):
    assert foo.config_key == "foo"


def test_config_key_with_config_in_class_name(foo: FooConfig):
    assert foo.config_key == "foo"
