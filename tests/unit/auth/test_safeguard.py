from unittest.mock import Mock

import pytest
from fastapi import Request
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer,
    OAuth2PasswordBearer,
)

from pyrannic.auth.safeguard import Safeguard


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
    result = await safeguard(request)

    assert isinstance(result, HTTPAuthorizationCredentials)
    assert result.scheme == "Bearer"
    assert result.credentials == "token"
