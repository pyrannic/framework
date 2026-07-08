from typing import Any

from pyrannic.support.collections.dot_dict import add


def test_add__without_nested_keys():
    d: dict[str, Any] = {}
    d = add(d, "a", 1)
    assert d["a"] == 1
    d = add(d, "b", 2)
    assert d["b"] == 2
    d = add(d, "c", 3)
    assert d["c"] == 3


def test_add__with_nested_keys():
    d: dict[str, Any] = {}
    d = add(d, "a.b", 1)
    assert d["a"]["b"] == 1
    d = add(d, "a.c", 2)
    assert d["a"]["c"] == 2
    d = add(d, "d.e.f", 3)
    assert d["d"]["e"]["f"] == 3
