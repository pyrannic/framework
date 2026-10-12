from typing import Any

from pyrannic.support.collections.dict import flatten


def test_flatten():
    """Test the flatten function with nested dictionaries of lists."""
    nested_dict: dict[str, list[Any]] = {
        "a": [1, 2],
        "b": [3, 4],
        "c": [5, 6],
    }
    assert flatten(nested_dict) == [1, 2, 3, 4, 5, 6]


def test_flatten_empty():
    """Test the flatten function with an empty dictionary."""
    nested_dict: dict[str, list[Any]] = {}
    assert flatten(nested_dict) == []


def test_flatten_with_nested_lists():
    """Test the flatten function with a nested lists."""
    nested_dict: dict[str, list[Any]] = {
        "a": [1, 2],
        "b": [3, 4],
        "c": [5, 6, [7, 8]],
    }
    assert flatten(nested_dict) == [1, 2, 3, 4, 5, 6, 7, 8]
