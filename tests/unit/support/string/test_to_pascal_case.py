import pytest
from pyrannic.support.string import to_pascal_case, to_studly_case


@pytest.mark.parametrize(
    "input_val,expected",
    [
        ("Hello World", "HelloWorld"),
        ("hello World Test", "HelloWorldTest"),
        ("HTTP Response Code", "HttpResponseCode"),
        ("already_snake", "AlreadySnake"),
        ("with spaces", "WithSpaces"),
        ("with-dash", "WithDash"),
        ("numbers123", "Numbers123"),
        ("", ""),
    ],
)
def test_to_pascal_case_various(input_val: str, expected: str) -> None:
    """Test the to_pascal_case function with various input strings."""
    assert to_pascal_case(input_val) == expected


@pytest.mark.parametrize(
    "input_val,expected",
    [
        ("Hello World", "HelloWorld"),
        ("hello World Test", "HelloWorldTest"),
        ("HTTP Response Code", "HttpResponseCode"),
        ("already_snake", "AlreadySnake"),
        ("with spaces", "WithSpaces"),
        ("with-dash", "WithDash"),
        ("numbers123", "Numbers123"),
        ("", ""),
    ],
)
def test_to_studly_case_various(input_val: str, expected: str) -> None:
    """Test the to_studly_case function with various input strings."""
    assert to_studly_case(input_val) == expected
