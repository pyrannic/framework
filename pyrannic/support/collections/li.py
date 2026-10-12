from typing import Any, cast


def wrap(value: Any) -> list[Any]:
    """Wrap a value in a list if it is not already a list. If the value is None, return an empty list."""
    if value is None:
        return []
    elif isinstance(value, list):
        return cast(list[Any], value)
    else:
        return [value]


def flatten(value: list[Any]) -> list[Any]:
    """Flatten a nested list into a single list."""
    result: list[Any] = []
    for item in value:
        if isinstance(item, list):
            result.extend(flatten(cast(list[Any], item)))
        else:
            result.append(item)
    return result
