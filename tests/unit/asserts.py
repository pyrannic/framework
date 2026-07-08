from typing import Any


def assert_instance_repr(instance: object, **kwargs: Any) -> None:
    repr_ = repr(instance)

    assert instance.__class__.__name__ in repr_

    for key, value in kwargs.items():
        assert f"{key}={value!r}" in repr_
