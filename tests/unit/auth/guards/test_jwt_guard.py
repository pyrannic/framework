from unittest.mock import Mock

import jwt
import pytest

from pyrannic.auth.guards.jwt_guard import JwtGuard
from pyrannic.auth.unauthorized_exception import UnauthorizedException
from pyrannic.contracts.application import ApplicationInterface
from pyrannic.contracts.config.repository import ConfigRepositoryInterface
from tests.conftest import MemoryUserProvider


@pytest.mark.asyncio
async def test_jwt_guard_empty(application: ApplicationInterface):
    provider = MemoryUserProvider()
    config: ConfigRepositoryInterface = await application.container.resolve("config")

    guard = JwtGuard(provider, config)
    assert guard.maybe_user is None
    assert guard.maybe_id is None
    assert guard.check is False
    assert guard.is_guest
    assert guard.validate("token", {}) is True
    assert guard.has_user is False


@pytest.mark.asyncio
async def test_jwt_guard_manually_authenticate_user(application: ApplicationInterface):
    provider = MemoryUserProvider()
    config: ConfigRepositoryInterface = await application.container.resolve("config")

    guard = JwtGuard(provider, config)

    user = await provider.retrieve_by_id(1)

    if user:
        guard.set_user(user)
    guard.set_provider(provider)

    assert guard.user is user
    assert guard.id == "1"
    assert guard.provider is provider


@pytest.mark.asyncio
async def test_jwt_guard_authenticate_user(
    application: ApplicationInterface,
    monkeypatch: pytest.MonkeyPatch,
):
    provider = MemoryUserProvider()

    config: ConfigRepositoryInterface = await application.container.resolve("config")

    guard = JwtGuard(provider, config)
    jwks_client = Mock()
    jwks_client.get_signing_key_from_jwt = Mock(return_value="secret")
    monkeypatch.setattr(guard, "_jwks_client", jwks_client)
    monkeypatch.setattr(jwt, "decode", Mock(return_value={"password": "secret"}))

    await guard.__ioc_call__(credentials=Mock(scheme="Bearer", credentials="secret"))

    user = await provider.retrieve_by_id(1)

    assert guard.user is user
    assert guard.id == "1"
    assert guard.provider is provider


@pytest.mark.asyncio
async def test_jwt_guard_user_raises_value_error(application: ApplicationInterface):
    provider = MemoryUserProvider()
    config: ConfigRepositoryInterface = await application.container.resolve("config")
    guard = JwtGuard(provider, config)

    with pytest.raises(ValueError) as exc_info:
        guard.user

    error = str(exc_info.value)
    assert "No user is currently authenticated" in error


@pytest.mark.asyncio
async def test_jwt_guard_missing_jwks_raises_runtime_error(
    application: ApplicationInterface,
):
    provider = MemoryUserProvider()

    config: ConfigRepositoryInterface = await application.container.resolve("config")
    config.set("auth.guards.jwt.jwks_url", None)  # Ensure JWKS URL is not set

    guard = JwtGuard(provider, config)

    with pytest.raises(RuntimeError) as exc_info:
        await guard.__ioc_call__(
            credentials=Mock(scheme="Bearer", credentials="secret")
        )

    error = str(exc_info.value)
    assert "JWKS URL is not configured for JWT guard" in error


@pytest.mark.asyncio
async def test_jwt_guard_jwks_client(
    application: ApplicationInterface,
):
    provider = MemoryUserProvider()

    config: ConfigRepositoryInterface = await application.container.resolve("config")
    config.set("auth.guards.jwt.jwks_url", "https://example.com/.well-known/jwks.json")

    guard = JwtGuard(provider, config)

    assert guard.jwks_client is not None
    assert isinstance(guard.jwks_client, jwt.PyJWKClient)
    assert guard.jwks_client.uri == "https://example.com/.well-known/jwks.json"


@pytest.mark.asyncio
async def test_jwt_guard_decode_raises_unauthorized_exception(
    application: ApplicationInterface,
    monkeypatch: pytest.MonkeyPatch,
):
    provider = MemoryUserProvider()

    config: ConfigRepositoryInterface = await application.container.resolve("config")
    config.set("auth.guards.jwt.jwks_url", "https://example.com/.well-known/jwks.json")

    guard = JwtGuard(provider, config)

    with pytest.raises(UnauthorizedException) as exc_info:
        await guard.__ioc_call__(
            credentials=Mock(scheme="Bearer", credentials="secret")
        )

    error = str(exc_info.value)
    assert "JWT validation failed" in error
