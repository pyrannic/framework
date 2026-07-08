from typing import Any

from pyrannic.support.collections.dot_dict import add, get


def test_get__without_nested_keys():
    d: dict[str, Any] = {}
    d = add(d, "a", 1)
    assert get(d, "a") == 1
    d = add(d, "b", 2)
    assert get(d, "b") == 2
    d = add(d, "c", 3)
    assert get(d, "c") == 3


def test_get__with_nested_keys():
    d: dict[str, Any] = {}
    d = add(d, "a.b", 1)
    assert get(d, "a.b") == 1
    d = add(d, "a.c", 2)
    assert get(d, "a.c") == 2
    d = add(d, "d.e.f", 3)
    assert get(d, "d.e.f") == 3
