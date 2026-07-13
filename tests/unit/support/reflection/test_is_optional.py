from typing import Optional

from pyrannic.support.reflection import is_optional


class FooClass:
    bar: str
    bar_optional: str | None
    bar_optional_with_annotation: Optional[str]
    bar_optional_with_default: str | None = None
    bar_optional_with_default_value: str | None = "default"


def test_is_optional():
    """Test the is_optional function with an optional attribute."""
    assert is_optional(FooClass, "bar") is False
    assert is_optional(FooClass, "foo_missing") is True
    assert is_optional(FooClass, "bar_optional") is True
    assert is_optional(FooClass, "bar_optional_with_annotation") is True
    assert is_optional(FooClass, "bar_optional_with_default") is True
    assert is_optional(FooClass, "bar_optional_with_default_value") is True
