from typing import Any, Callable

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

from pyrannic.container.container import Container
from pyrannic.contracts.application import ApplicationInterface


class ForgetScopedInstancesMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable[..., Any]) -> Any:
        response = await call_next(request)

        if isinstance(request.app, ApplicationInterface) and isinstance(
            request.app.container, Container
        ):
            request.app.container.forget_scoped_instances()

        return response
