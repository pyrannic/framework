from app.http.middlewares.middleware_a import A_Middleware
from app.http.middlewares.middleware_b import B_Middleware
from app.http.middlewares.middleware_c import C_Middleware
from app.http.middlewares.middleware_func import middleware_func


middlewares: list[object] = [
    B_Middleware,
    middleware_func,
    C_Middleware,
    A_Middleware,
]

__all__ = ["middlewares"]
