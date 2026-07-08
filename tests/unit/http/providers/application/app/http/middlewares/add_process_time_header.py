import time
from typing import Any, Callable

from fastapi import Request


async def add_process_time_header(
    request: Request,
    call_next: Callable[..., Any],
) -> Any:
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response
