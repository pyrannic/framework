from typing import Any

import pytest


@pytest.fixture(scope="module")
def items() -> list[Any]:
    return []
