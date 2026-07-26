from typing import Any, Callable

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware


class B_Middleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable[..., Any]) -> Any:
        response = await call_next(request)
        return response
