from tests.unit.config.configuration.foo import Foo


def test_to_dict(foo: Foo):
    assert foo.to_dict() == {
        "name": "MyFooApp",
        "env": "development",
        "debug": True,
        "session_lifetime": 120,
        "cors_allowed_methods": ["GET", "POST"],
        "allowed_ports": [7070, 8080, 9090],
    }
