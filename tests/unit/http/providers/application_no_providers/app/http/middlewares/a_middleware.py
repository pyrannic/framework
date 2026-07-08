from typing import Any, Callable

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware


class AMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable[..., Any]) -> Any:
        print("A_Middleware: Before request")
        response = await call_next(request)
        print("A_Middleware: After request")
        return response
