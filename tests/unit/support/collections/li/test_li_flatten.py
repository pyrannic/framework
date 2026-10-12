from typing import Any

from pyrannic.support.collections import li


def test_flatten():
    """Test the flatten function with nested lists."""
    nested_list: list[Any] = [1, [2, 3], [4, [5, 6]]]
    assert li.flatten(nested_list) == [1, 2, 3, 4, 5, 6]
