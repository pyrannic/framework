from pydantic import ValidationError
import pytest

from pyrannic.pagination import PaginationMeta
from tests.unit.asserts import assert_instance_repr


def test_meta_with_defaults():
    meta = PaginationMeta(
        current_page=1,
        last_page=10,
        total=100,
        from_index=0,
        to_index=9,
    )

    assert meta.per_page == 15


def test_meta_with_passing_all_values():
    meta = PaginationMeta(
        current_page=1,
        last_page=10,
        per_page=20,
        total=100,
        from_index=0,
        to_index=9,
    )

    assert meta.current_page == 1
    assert meta.last_page == 10
    assert meta.per_page == 20
    assert meta.total == 100
    assert meta.from_index == 0
    assert meta.to_index == 9


def test_meta_representation():
    data = {
        "current_page": 1,
        "last_page": 10,
        "per_page": 20,
        "total": 100,
        "from_index": 0,
        "to_index": 9,
    }

    meta = PaginationMeta(**data)

    assert_instance_repr(meta, **data)


def test_meta_invalid_per_page():
    data = {
        "per_page": 0,
        "current_page": 1,
        "last_page": 10,
        "total": 100,
        "from_index": 0,
        "to_index": 9,
    }
    with pytest.raises(ValidationError) as exc_info:
        PaginationMeta(**data)

    error = str(exc_info.value)

    assert "per_page" in error
    assert "Input should be greater than or equal to 1" in error


def test_meta_invalid_current_page():
    data = {
        "current_page": 0,
        "last_page": 10,
        "total": 100,
        "from_index": 0,
        "to_index": 9,
    }
    with pytest.raises(ValidationError) as exc_info:
        PaginationMeta(**data)

    error = str(exc_info.value)

    assert "current_page" in error
    assert "Input should be greater than or equal to 1" in error


def test_meta_invalid_last_page():
    data = {
        "current_page": 1,
        "last_page": 0,
        "total": 100,
        "from_index": 0,
        "to_index": 9,
    }
    with pytest.raises(ValidationError) as exc_info:
        PaginationMeta(**data)

    error = str(exc_info.value)

    assert "last_page" in error
    assert "Input should be greater than or equal to 1" in error


def test_meta_last_page_smaller_than_current_page():
    data = {
        "current_page": 11,
        "last_page": 10,
        "total": 100,
        "from_index": 0,
        "to_index": 9,
    }
    with pytest.raises(ValidationError) as exc_info:
        PaginationMeta(**data)

    error = str(exc_info.value)

    assert "last_page must be greater than or equal to current_page" in error


def test_meta_in_the_last_page():
    data = {
        "current_page": 10,
        "last_page": 10,
        "total": 100,
        "from_index": 90,
        "to_index": 99,
    }
    meta = PaginationMeta(**data)

    assert meta.current_page == 10
    assert meta.last_page == 10
    assert meta.per_page == 15
    assert meta.total == 100
    assert meta.from_index == 90
    assert meta.to_index == 99
