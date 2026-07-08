from typing import Any


def add(dict_: dict[str, Any], key: str, value: Any) -> dict[str, Any]:
    """
    Add a value to a dictionary using "dot" notation.

    Args:
        dict_: The dictionary to add the value to.
        key: The key under which to add the value.
        value: The value to add to the dictionary.
    """
    if not has(dict_, key):
        set(dict_, key, value)

    return dict_


def has(dict_: dict[str, Any], key: str) -> bool:
    """Check if a dictionary has a given item using "dot" notation."""
    return get(dict_, key) is not None


def get(dict_: dict[str, Any], key: str, default: Any | None = None) -> Any | None:
    """Get an item from a dictionary using "dot" notation."""
    keys = key.split(".")
    d = dict_
    for k in keys:
        if not _is_accessible(d) or k not in d:
            return default
        d = d[k]

    return d


def set(dict_: dict[str, Any], key: str, value: Any) -> dict[str, Any]:
    """Set a dict item to a given value using "dot" notation."""

    keys = key.split(".")
    d = dict_
    for k in keys[:-1]:
        if k not in d or not isinstance(d[k], dict):
            d[k] = {}
        d = d[k]

    d[keys[-1]] = value

    return d


def _is_accessible(dict_: Any) -> bool:
    """Determine whether the given value is dictionary accessible."""
    return isinstance(dict_, dict)
