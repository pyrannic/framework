from typing import Any


def resolve_value(val: Any) -> Any:
    return val() if callable(val) else val
