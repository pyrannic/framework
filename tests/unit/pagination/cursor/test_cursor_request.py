from typing import Any

import pytest
from pydantic import ValidationError

from pyrannic.pagination.cursor import PaginationRequest


def test_request_with_defaults():
    request = PaginationRequest()

    assert request.page is None
    assert request.per_page == 15


def test_request_passing_all_values():
    data: dict[str, Any] = {
        "page": "cursor-1",
        "per_page": 10,
    }

    request = PaginationRequest(**data)

    assert request.page == data["page"]
    assert request.per_page == data["per_page"]


def test_request_passing_only_page():
    data: dict[str, Any] = {
        "page": "cursor-1",
    }

    request = PaginationRequest(**data)

    assert request.page == data["page"]
    assert request.per_page == 15


def test_request_passing_only_per_page():
    data: dict[str, Any] = {
        "per_page": 10,
    }

    request = PaginationRequest(**data)

    assert request.page is None
    assert request.per_page == data["per_page"]


def test_request_invalid_per_page():
    data: dict[str, Any] = {
        "page": "cursor-1",
        "per_page": 0,
    }

    with pytest.raises(ValidationError) as exc_info:
        PaginationRequest(**data)

    error = str(exc_info.value)

    assert "per_page" in error
    assert "Input should be greater than or equal to 1" in error
