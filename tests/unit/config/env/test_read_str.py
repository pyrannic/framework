from pyrannic.config.env import read_str


def test_read_str():
    assert read_str("FOO_NAME") == "MyFooApp"


def test_read_str_with_default():
    assert read_str("FOO_APP_NAME", default="DefaultFooApp") == "DefaultFooApp"


def test_read_str_not_found():
    assert read_str("FOO_APP_NAME") == ""
