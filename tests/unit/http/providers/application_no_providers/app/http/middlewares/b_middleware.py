from typing import Any, Callable

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware


class BMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable[..., Any]) -> Any:
        print("B_Middleware: Before request")
        response = await call_next(request)
        print("B_Middleware: After request")
        return response
