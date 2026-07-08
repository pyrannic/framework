from datetime import datetime

import pytest

from pyrannic.pagination.paginator import Paginator
from tests.unit.http.resources.utils import (
    BarCollection,
    FooCollection,
    FooResource,
    FooModel,
)


def test_collection__using_explicit_resource_cls():
    created_at = datetime.now()

    collection = FooCollection(
        [
            FooModel(
                id=1,
                name="Resource 1",
                created_at=created_at,
                updated_at=created_at,
            ),
            FooModel(
                id=2,
                name="Resource 2",
                created_at=created_at,
                updated_at=created_at,
            ),
        ]
    )

    assert isinstance(collection, FooCollection)
    assert isinstance(collection.data[0], FooResource)
    assert collection.__resource_cls__ is FooResource
    assert collection.__meta_cls__ is not None


def test_collection__using_inferred_resource_cls():
    created_at = datetime.now()

    collection = BarCollection(
        [
            FooModel(
                id=1,
                name="Resource 1",
                created_at=created_at,
                updated_at=created_at,
            ),
            FooModel(
                id=2,
                name="Resource 2",
                created_at=created_at,
                updated_at=created_at,
            ),
        ]
    )

    assert isinstance(collection, BarCollection)
    assert isinstance(collection.data[0], FooResource)
    assert collection.__meta_cls__ is not None

    with pytest.raises(AttributeError) as exc_info:
        collection.__resource_cls__

    error = str(exc_info.value)
    assert "'BarCollection' object has no attribute '__resource_cls__'" in error


def test_collection__empty():
    collection = FooCollection([])

    assert isinstance(collection, FooCollection)
    assert len(collection.data) == 0
    assert collection.__meta_cls__ is not None


def test_collection__init_with_paginator():
    created_at = datetime.now()

    items = [
        FooModel(
            id=1,
            name="Resource 1",
            created_at=created_at,
            updated_at=created_at,
        ),
        FooModel(
            id=2,
            name="Resource 2",
            created_at=created_at,
            updated_at=created_at,
        ),
    ]

    paginator = Paginator(items)
    collection = FooCollection(paginator)

    assert isinstance(collection, FooCollection)
    assert isinstance(collection.data[0], FooResource)
    assert collection.__resource_cls__ is FooResource
    assert collection.__meta_cls__ is not None
