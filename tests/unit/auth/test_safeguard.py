from unittest.mock import MagicMock, Mock, PropertyMock

import pytest
from fastapi import Request
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer,
    OAuth2PasswordBearer,
)

from pyrannic.auth import Safeguard, UnauthorizedException
from pyrannic.contracts.auth.access.gate import GateInterface
from pyrannic.contracts.auth.guard import GuardInterface


def test_safeguard_raise_runtime_error():
    # Reset the security model to None
    Safeguard._security_model = None  # pyright: ignore[reportPrivateUsage]

    with pytest.raises(RuntimeError) as exc_info:
        Safeguard()

    error = str(exc_info.value)
    assert "No security model has been set." in error
    assert "Please use Safeguard.use_security_model() to set one." in error


def test_safeguard_security_model():
    model = OAuth2PasswordBearer(tokenUrl="token")

    Safeguard.use_security_model(model)
    assert Safeguard.get_security_model() == model


def test_safeguard_instance():
    model = OAuth2PasswordBearer(tokenUrl="token")
    Safeguard.use_security_model(model)

    safeguard = Safeguard()

    assert safeguard.model == model.model
    assert safeguard.scheme_name == model.scheme_name


@pytest.mark.asyncio
async def test_safeguard_call():
    model = HTTPBearer()
    Safeguard.use_security_model(model)

    safeguard = Safeguard()
    request = Mock(spec=Request)
    request.headers = {"Authorization": "Bearer token"}

    guard = Mock(spec=GuardInterface)
    gate = Mock(spec=GateInterface)

    result = await safeguard(request, guard, gate)

    assert isinstance(result, HTTPAuthorizationCredentials)
    assert result.scheme == "Bearer"
    assert result.credentials == "token"


@pytest.mark.asyncio
async def test_safeguard_call_raises_unauthorized_exception():
    model = HTTPBearer(auto_error=False)
    Safeguard.use_security_model(model)

    safeguard = Safeguard()
    request = Mock(spec=Request)
    request.headers = {}

    guard = MagicMock(spec=GuardInterface)
    gate = Mock(spec=GateInterface)

    type(guard).maybe_user = PropertyMock(return_value=None)

    with pytest.raises(UnauthorizedException) as exc_info:
        await safeguard(request, guard, gate)

    error = str(exc_info.value)
    assert "401: This action is unauthorized." in error


@pytest.mark.asyncio
async def test_safeguard_allow_guests():
    model = HTTPBearer(auto_error=False)
    Safeguard.use_security_model(model)

    safeguard = Safeguard(allow_guests=True)
    request = Mock(spec=Request)
    request.headers = {}

    guard = MagicMock(spec=GuardInterface)
    gate = Mock(spec=GateInterface)

    type(guard).maybe_user = PropertyMock(return_value=None)

    result = await safeguard(request, guard, gate)

    assert result is None
