import os
from typing import Any, Sequence


def read_str(key: str, default: str | None = "") -> str:
    """Read a string value from environment variables."""

    return os.environ.get(key, default or "")


def read_int(key: str, default: int | None = 0) -> int:
    """Read an integer value from environment variables."""

    value = os.environ.get(key)

    if value is None:
        return default or 0
    else:
        try:
            return int(value)
        except ValueError:
            raise ValueError(f"Invalid integer value for {key}: {value}")


def read_bool(key: str, default: bool = False) -> bool:
    """Read a boolean value from environment variables."""

    value = os.environ.get(key, str(default))
    val_lower = value.lower()

    if val_lower in ("true", "1", "yes"):
        return True
    elif val_lower in ("false", "0", "no"):
        return False
    else:
        raise ValueError(f"Invalid boolean value for {key}: {value}")


def read_seq(key: str, default: Sequence[Any] | None = None) -> Sequence[Any]:
    """Read a sequence from environment variables, split by commas."""

    value = os.environ.get(key)

    if value is None:
        return default or ()
    else:
        values = ()

        for item in value.split(","):
            item = item.strip()
            if item:
                values += (item,)

        return values
