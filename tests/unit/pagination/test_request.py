from pydantic import ValidationError
import pytest

from pyrannic.pagination import PaginationRequest


def test_request_with_defaults():
    request = PaginationRequest()

    assert request.page == 1
    assert request.per_page == 15


def test_request_passing_all_values():
    data = {
        "page": 1,
        "per_page": 10,
    }

    request = PaginationRequest(**data)

    assert request.page == data["page"]
    assert request.per_page == data["per_page"]


def test_request_passing_only_page():
    data = {
        "page": 1,
    }

    request = PaginationRequest(**data)

    assert request.page == data["page"]
    assert request.per_page == 15


def test_request_passing_only_per_page():
    data = {
        "per_page": 10,
    }

    request = PaginationRequest(**data)

    assert request.page == 1
    assert request.per_page == data["per_page"]


def test_request_invalid_page():
    data = {
        "page": 0,
        "per_page": 10,
    }
    with pytest.raises(ValidationError) as exc_info:
        PaginationRequest(**data)

    error = str(exc_info.value)

    assert "page" in error
    assert "Input should be greater than or equal to 1" in error


def test_request_invalid_per_page():
    data = {
        "page": 1,
        "per_page": 0,
    }
    with pytest.raises(ValidationError) as exc_info:
        PaginationRequest(**data)

    error = str(exc_info.value)

    assert "per_page" in error
    assert "Input should be greater than or equal to 1" in error
