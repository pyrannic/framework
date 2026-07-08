import pytest
from pyrannic.support.string import to_camel_case


@pytest.mark.parametrize(
    "input_val,expected",
    [
        ("Hello World", "helloWorld"),
        ("hello World Test", "helloWorldTest"),
        ("HTTP Response Code", "httpResponseCode"),
        ("already_snake", "alreadySnake"),
        ("with spaces", "withSpaces"),
        ("with-dash", "withDash"),
        ("numbers123", "numbers123"),
        ("", ""),
    ],
)
def test_to_camel_case_various(input_val: str, expected: str) -> None:
    """Test the to_camel_case function with various input strings."""
    assert to_camel_case(input_val) == expected
