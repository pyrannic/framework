from collections.abc import Callable
from inspect import isawaitable
from typing import Any

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

from pyrannic.container.container import Container
from pyrannic.contracts.application import ApplicationInterface


class ForgetScopedInstancesMiddleware(BaseHTTPMiddleware):
    async def _close_if_possible(self, value: Any) -> None:
        close = getattr(value, "aclose", None)
        if callable(close):
            result = close()
            if isawaitable(result):
                await result
            return

        close = getattr(value, "close", None)
        if callable(close):
            result = close()
            if isawaitable(result):
                await result

    async def dispatch(self, request: Request, call_next: Callable[..., Any]) -> Any:
        container: Container | None = None

        if isinstance(request.app, ApplicationInterface) and isinstance(
            request.app.container, Container
        ):
            container = request.app.container
            container.forget_scoped_instances()

        try:
            return await call_next(request)
        finally:
            seen: set[int] = set()

            scoped_instances = getattr(request.state, "_pyrannic_scoped_instances", {})
            for instance in scoped_instances.values():
                obj_id = id(instance)
                if obj_id in seen:
                    continue

                seen.add(obj_id)
                await self._close_if_possible(instance)

            dependency_cache = getattr(request.state, "_pyrannic_dependency_cache", {})
            for value in dependency_cache.values():
                obj_id = id(value)
                if obj_id in seen:
                    continue

                seen.add(obj_id)
                await self._close_if_possible(value)

            fallback_stack = getattr(request.state, "_pyrannic_async_exit_stack", None)
            if fallback_stack is not None:
                await fallback_stack.aclose()

            if hasattr(request.state, "_pyrannic_dependency_cache"):
                delattr(request.state, "_pyrannic_dependency_cache")

            if hasattr(request.state, "_pyrannic_scoped_instances"):
                delattr(request.state, "_pyrannic_scoped_instances")

            if container:
                container.forget_scoped_instances()
