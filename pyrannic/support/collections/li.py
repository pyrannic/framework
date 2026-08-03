from typing import Any, cast


def wrap(value: Any) -> list[Any]:
    """Wrap a value in a list if it is not already a list. If the value is None, return an empty list."""
    if value is None:
        return []
    elif isinstance(value, list):
        return cast(list[Any], value)
    else:
        return [value]
