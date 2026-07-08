import pytest
from pyrannic.support.string import to_snake_case


@pytest.mark.parametrize(
    "input_val,expected",
    [
        ("HelloWorld", "hello_world"),
        ("helloWorldTest", "hello_world_test"),
        ("HTTPResponseCode", "httpresponse_code"),
        ("already_snake", "already_snake"),
        ("with spaces", "with_spaces"),
        ("with-dash", "with_dash"),
        ("numbers123", "numbers"),
        ("", ""),
    ],
)
def test_to_snake_case_various(input_val: str, expected: str) -> None:
    """Test the to_snake_case function with various input strings."""
    assert to_snake_case(input_val) == expected
