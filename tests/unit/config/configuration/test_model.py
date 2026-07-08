from tests.unit.config.configuration.foo import Foo


def test_model(foo: Foo):
    assert foo.cors_allowed_methods == ["GET", "POST"]
