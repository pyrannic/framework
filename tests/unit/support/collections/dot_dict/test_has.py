from typing import Any

from pyrannic.support.collections.dot_dict import add, has


def test_has__without_nested_keys():
    d: dict[str, Any] = {}
    d = add(d, "a", 1)
    assert has(d, "a")
    d = add(d, "b", 2)
    assert has(d, "b")
    d = add(d, "c", 3)
    assert has(d, "c")


def test_has__with_nested_keys():
    d: dict[str, Any] = {}
    d = add(d, "a.b", 1)
    assert has(d, "a.b")
    d = add(d, "a.c", 2)
    assert has(d, "a.c")
    d = add(d, "d.e.f", 3)
    assert has(d, "d.e.f")
