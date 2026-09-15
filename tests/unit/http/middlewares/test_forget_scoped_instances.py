from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock

import pytest
from fastapi import FastAPI, Request

from pyrannic import Application
from pyrannic.http.middlewares.forget_scoped_instances import (
    ForgetScopedInstancesMiddleware,
)


def _build_request(app: FastAPI) -> Request:
    return Request({"type": "http", "app": app})


@pytest.mark.asyncio
async def test_dispatch_forgets_scoped_instances_and_cleans_request_state() -> None:
    app = Application(base_path="tests/application")
    container = app.container
    container.forget_scoped_instances = MagicMock()  # pyright: ignore[reportAttributeAccessIssue]

    middleware = ForgetScopedInstancesMiddleware(app)
    request = _build_request(app)

    async_close = SimpleNamespace(aclose=AsyncMock())
    close_async = SimpleNamespace(close=AsyncMock())
    close_sync = SimpleNamespace(close=MagicMock())
    no_close = object()

    request.state._pyrannic_scoped_instances = {
        "first": async_close,
        "duplicate": async_close,
        "sync": close_sync,
    }
    request.state._pyrannic_dependency_cache = {
        "async_close": close_async,
        "duplicate": async_close,
        "none": no_close,
    }

    fallback_stack = SimpleNamespace(aclose=AsyncMock())
    request.state._pyrannic_async_exit_stack = fallback_stack

    async def call_next(_: Request) -> dict[str, bool]:
        return {"ok": True}

    response = await middleware.dispatch(request, call_next)

    assert response == {"ok": True}
    assert container.forget_scoped_instances.call_count == 2  # pyright: ignore[reportAttributeAccessIssue]
    async_close.aclose.assert_awaited_once()
    close_async.close.assert_awaited_once()
    close_sync.close.assert_called_once_with()
    fallback_stack.aclose.assert_awaited_once()
    assert not hasattr(request.state, "_pyrannic_dependency_cache")
    assert not hasattr(request.state, "_pyrannic_scoped_instances")


@pytest.mark.asyncio
async def test_dispatch_without_application_interface_still_returns_response() -> None:
    app = FastAPI()
    middleware = ForgetScopedInstancesMiddleware(app)
    request = _build_request(app)

    async def call_next(_: Request) -> str:
        return "ok"

    response = await middleware.dispatch(request, call_next)

    assert response == "ok"


@pytest.mark.asyncio
async def test_dispatch_runs_finally_when_downstream_raises() -> None:
    app = FastAPI()
    middleware = ForgetScopedInstancesMiddleware(app)
    request = _build_request(app)

    close_async = SimpleNamespace(close=AsyncMock())
    request.state._pyrannic_dependency_cache = {"resource": close_async}

    async def call_next(_: Request) -> None:
        raise RuntimeError("boom")

    with pytest.raises(RuntimeError, match="boom"):
        await middleware.dispatch(request, call_next)

    close_async.close.assert_awaited_once()
    assert not hasattr(request.state, "_pyrannic_dependency_cache")
