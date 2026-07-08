from typing import Any

from pyrannic.pagination import Paginator
from tests.unit.asserts import assert_instance_repr


def test_paginator_items(items: list[Any]):
    paginator = Paginator(
        items=items,
    )
    assert paginator.items == items


def test_paginator_meta(items: list[Any]):
    paginator = Paginator(
        items=items,
        page=1,
        per_page=15,
        total=100,
        last_page=7,
    )
    meta = paginator.meta()
    assert meta.current_page == 1
    assert meta.last_page == 7
    assert meta.per_page == 15
    assert meta.total == 100
    assert meta.from_index == 1
    assert meta.to_index == 15


def test_paginator_representation(items: list[Any]):
    data: dict[str, Any] = {
        "items": items,
    }

    paginator = Paginator(**data)
    meta = paginator.meta()

    assert_instance_repr(paginator, meta=meta)
