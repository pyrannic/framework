from typing import Any

from pyrannic.support.collections import li


def flatten(values: dict[str, list[Any]]) -> list[Any]:
    """Flatten a dictionary of lists into a single list of values."""
    return li.flatten([item for sublist in values.values() for item in sublist])
