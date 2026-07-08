import re


def to_snake_case(value: str) -> str:
    """Convert a string to snake case."""

    value = (
        re.sub(r"(?<=[a-z])(?=[A-Z])|[^a-zA-Z]", " ", value).strip().replace(" ", "_")
    )

    return "".join(value.lower())


def to_camel_case(value: str) -> str:
    """Convert a string to camel case."""

    value = re.sub(r"[^a-zA-Z0-9]", " ", value).title().replace(" ", "")
    return value[0].lower() + value[1:] if value else ""


def to_pascal_case(value: str) -> str:
    """Convert a string to Pascal case. Alias for studly case function: to_studly_case"""

    value = re.sub(r"[^a-zA-Z0-9]", " ", value).title().replace(" ", "")
    return value


def to_studly_case(value: str) -> str:
    """Convert a string to studly case. Alias for Pascal case function: to_pascal_case"""

    return to_pascal_case(value)
