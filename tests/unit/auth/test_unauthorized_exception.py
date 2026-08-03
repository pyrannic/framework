from pyrannic.auth.unauthorized_exception import UnauthorizedException


def test_unauthorized_exception():
    exception = UnauthorizedException()

    assert exception.detail == "This action is unauthorized."
    assert exception.status_code == 401


def test_unauthorized_exception_with_custom_message():
    exception = UnauthorizedException(message="Custom unauthorized message.")

    assert exception.detail == "Custom unauthorized message."
    assert exception.status_code == 401


def test_unauthorized_exception_with_custom_headers():
    custom_headers = {"X-Custom-Header": "CustomValue"}
    exception = UnauthorizedException(headers=custom_headers)

    assert exception.detail == "This action is unauthorized."
    assert exception.status_code == 401
    assert exception.headers == custom_headers
