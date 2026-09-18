from typing import Any

from pyrannic.pagination.cursor import Paginator
from tests.unit.asserts import assert_instance_repr


def test_paginator_items(items: list[Any]):
    paginator = Paginator(
        items=items,
    )

    assert paginator.items == items


def test_paginator_meta(items: list[Any]):
    paginator = Paginator(
        items=items,
        previous_page="cursor-prev",
        next_page="cursor-next",
        per_page=15,
        total=100,
    )

    meta = paginator.meta()

    assert meta.previous_page == "cursor-prev"
    assert meta.next_page == "cursor-next"
    assert meta.per_page == 15
    assert meta.total == 100


def test_paginator_representation(items: list[Any]):
    data: dict[str, Any] = {
        "items": items,
    }

    paginator = Paginator(**data)
    meta = paginator.meta()

    assert_instance_repr(paginator, meta=meta)
