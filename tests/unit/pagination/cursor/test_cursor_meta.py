from typing import Any

import pytest
from pydantic import ValidationError

from pyrannic.pagination.cursor import PaginationMeta
from tests.unit.asserts import assert_instance_repr


def test_meta_with_defaults():
    meta = PaginationMeta()

    assert meta.previous_page is None
    assert meta.next_page is None
    assert meta.per_page == 15
    assert meta.total is None


def test_meta_with_passing_all_values():
    meta = PaginationMeta(
        previous_page="cursor-prev",
        next_page="cursor-next",
        per_page=20,
        total=100,
    )

    assert meta.previous_page == "cursor-prev"
    assert meta.next_page == "cursor-next"
    assert meta.per_page == 20
    assert meta.total == 100


def test_meta_representation():
    data: dict[str, Any] = {
        "previous_page": "cursor-prev",
        "next_page": "cursor-next",
        "per_page": 20,
        "total": 100,
    }

    meta = PaginationMeta(**data)

    assert_instance_repr(meta, **data)


def test_meta_invalid_per_page():
    data: dict[str, Any] = {
        "per_page": 0,
        "total": 100,
    }

    with pytest.raises(ValidationError) as exc_info:
        PaginationMeta(**data)

    error = str(exc_info.value)

    assert "per_page" in error
    assert "Input should be greater than or equal to 1" in error


def test_meta_invalid_total():
    data: dict[str, Any] = {
        "per_page": 15,
        "total": -1,
    }

    with pytest.raises(ValidationError) as exc_info:
        PaginationMeta(**data)

    error = str(exc_info.value)

    assert "total" in error
    assert "Input should be greater than or equal to 0" in error
