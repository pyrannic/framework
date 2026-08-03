from pyrannic.auth.forbidden_exception import ForbiddenException


def test_forbidden_exception():
    exception = ForbiddenException()

    assert exception.detail == "This action is forbidden."
    assert exception.status_code == 403


def test_forbidden_exception_with_custom_message():
    exception = ForbiddenException(message="Custom forbidden message.")

    assert exception.detail == "Custom forbidden message."
    assert exception.status_code == 403


def test_forbidden_exception_with_custom_headers():
    custom_headers = {"X-Custom-Header": "CustomValue"}
    exception = ForbiddenException(headers=custom_headers)

    assert exception.detail == "This action is forbidden."
    assert exception.status_code == 403
    assert exception.headers == custom_headers
