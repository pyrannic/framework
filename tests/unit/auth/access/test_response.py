import pytest

from pyrannic.auth.access.response import Response
from pyrannic.auth.forbidden_exception import ForbiddenException


def test_response_allow():
    response = Response.allow("Access granted", 200).with_status(200)

    assert response.allowed is True
    assert response.denied is False
    assert response.message == "Access granted"
    assert response.code == 200
    assert response.status == 200


def test_response_deny():
    response = Response.deny("Access denied", 403).with_status(403)

    assert response.allowed is False
    assert response.denied is True
    assert response.message == "Access denied"
    assert response.code == 403
    assert response.status == 403


def test_response_authorize_allows():
    response = Response.allow("Access granted", 200).with_status(200)
    assert response.authorize() is response


def test_response_authorize_denies():
    response = Response.deny("Access denied", 403).with_status(403)

    with pytest.raises(ForbiddenException) as exc_info:
        response.authorize()

    error = str(exc_info.value)
    assert "Access denied" in error
