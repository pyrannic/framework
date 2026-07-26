import pytest

from pyrannic.support.string import to_kebab_case


@pytest.mark.parametrize(
    "input_val,expected",
    [
        ("HelloWorld", "hello-world"),
        ("Hello World", "hello-world"),
        ("hello World Test", "hello-world-test"),
        ("HTTP Response Code", "http-response-code"),
        ("already_snake", "already-snake"),
        ("with spaces", "with-spaces"),
        ("with-dash", "with-dash"),
        ("numbers123", "numbers123"),
        ("Numbers123Numbers", "numbers123numbers"),
        ("", ""),
    ],
)
def test_to_kebab_case_various(input_val: str, expected: str) -> None:
    """Test the to_kebab_case function with various input strings."""
    assert to_kebab_case(input_val) == expected
