import pytest

from pyrannic.auth.base_guard import BaseGuard
from tests.unit.auth.conftest import MemoryUserProvider


def test_base_guard_empty():
    guard = BaseGuard()
    assert guard.maybe_user is None
    assert guard.maybe_id is None
    assert guard.check is False
    assert guard.is_guest
    assert guard.validate({}) is False
    assert guard.has_user is False


@pytest.mark.asyncio
async def test_base_guard_authenticate_user():
    guard = BaseGuard()
    provider = MemoryUserProvider()

    user = await provider.retrieve_by_id(1)

    if user:
        guard.set_user(user)
    guard.set_provider(provider)

    assert guard.user is user
    assert guard.id == "1"
    assert guard.provider is provider


def test_base_guard_user_raises_value_error():
    guard = BaseGuard()

    with pytest.raises(ValueError) as exc_info:
        guard.user

    error = str(exc_info.value)
    assert "No user is currently authenticated" in error


def test_base_guard_provider_raises_value_error():
    guard = BaseGuard()

    with pytest.raises(ValueError) as exc_info:
        guard.provider

    error = str(exc_info.value)
    assert "Provider has not been set" in error
