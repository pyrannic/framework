from pyrannic.config.env import read_seq


def test_read_seq():
    assert read_seq("FOO_CORS_ALLOWED_METHODS") == ("GET", "POST")


def test_read_seq_with_default():
    assert read_seq("CORS_ALLOWED_METHODS", default=("GET", "POST", "PUT")) == (
        "GET",
        "POST",
        "PUT",
    )


def test_read_seq_not_found():
    assert len(read_seq("CORS_ALLOWED_METHODS")) == 0
