from tests.application.app.http.middlewares.add_process_time_header import (
    add_process_time_header,
)
from tests.application.app.http.middlewares.middleware_a import A_Middleware
from tests.application.app.http.middlewares.middleware_b import B_Middleware


middlewares: list[object] = [
    A_Middleware,
    B_Middleware,
    add_process_time_header,
]
