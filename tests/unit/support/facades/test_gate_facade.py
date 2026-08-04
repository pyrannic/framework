import pytest

from pyrannic.contracts.application import ApplicationInterface
from pyrannic.contracts.auth.access.gate import GateInterface
from pyrannic.facades import Gate
from tests.conftest import setup_auth


def test_get_facade_accessor():
    assert Gate.facade_accessor == GateInterface  # pyright: ignore[reportAttributeAccessIssue, reportUnknownMemberType]


@pytest.mark.asyncio
async def test_get_facade_root(gate: GateInterface):
    assert Gate._get_facade_root() == gate  # pyright: ignore[reportAttributeAccessIssue, reportUnknownMemberType]


@pytest.mark.asyncio
async def test_gate_has(application: ApplicationInterface):
    await setup_auth(application)

    assert Gate.has("create-post")
    assert Gate.has("update-post", "delete-post")
    assert not Gate.has("non-existent-ability")
