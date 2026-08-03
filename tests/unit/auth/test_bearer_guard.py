from unittest.mock import Mock

import pytest

from pyrannic.auth.bearer_guard import BearerGuard
from tests.unit.auth.conftest import MemoryUserProvider


def test_bearer_guard_empty():
    provider = MemoryUserProvider()

    guard = BearerGuard(provider)
    assert guard.maybe_user is None
    assert guard.maybe_id is None
    assert guard.check is False
    assert guard.is_guest
    assert guard.validate({}) is False
    assert guard.has_user is False


@pytest.mark.asyncio
async def test_bearer_guard_manually_authenticate_user():
    provider = MemoryUserProvider()
    guard = BearerGuard(provider)

    user = await provider.retrieve_by_id(1)

    if user:
        guard.set_user(user)
    guard.set_provider(provider)

    assert guard.user is user
    assert guard.id == "1"
    assert guard.provider is provider


@pytest.mark.asyncio
async def test_bearer_guard_authenticate_user():
    provider = MemoryUserProvider()
    guard = BearerGuard(provider)

    await guard.__ioc_call__(credentials=Mock(scheme="Bearer", credentials="secret"))

    user = await provider.retrieve_by_id(1)

    assert guard.user is user
    assert guard.id == "1"
    assert guard.provider is provider


def test_bearer_guard_user_raises_value_error():
    provider = MemoryUserProvider()
    guard = BearerGuard(provider)

    with pytest.raises(ValueError) as exc_info:
        guard.user

    error = str(exc_info.value)
    assert "No user is currently authenticated" in error
