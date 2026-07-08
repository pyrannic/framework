from typing import Any

from pyrannic.support.collections.dot_dict import set


def test_set__without_nested_keys():
    d: dict[str, Any] = {}
    d = set(d, "a", 1)
    assert d["a"] == 1
    d = set(d, "b", 2)
    assert d["b"] == 2
    d = set(d, "c", 3)
    assert d["c"] == 3


def test_set__with_nested_keys():
    d: dict[str, Any] = {}

    set(d, "a.b", 1)
    assert d["a"]["b"] == 1
    set(d, "a.c", 2)
    assert d["a"]["c"] == 2
    set(d, "d.e.f", 3)
    assert d["d"]["e"]["f"] == 3
