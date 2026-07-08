from tests.unit.config.configuration.foo import Foo
from tests.unit.config.configuration.foo_config import FooConfig


def test_env_prefix(foo: Foo):
    assert foo.env_prefix == "FOO_"


def test_env_prefix_with_config_in_class_name(foo: FooConfig):
    assert foo.env_prefix == "FOO_"
