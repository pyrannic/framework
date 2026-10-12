from pyrannic.support.collections import li


def test_li_wrap_with_none_value():
    """Test the wrap function with a None value."""
    assert li.wrap(None) == []


def test_li_wrap_with_single_value():
    """Test the wrap function with a single non-list value."""
    assert li.wrap(1) == [1]


def test_li_wrap_with_list_value():
    """Test the wrap function with a list value."""
    value = [1, 2, 3]
    assert li.wrap(value) == value
