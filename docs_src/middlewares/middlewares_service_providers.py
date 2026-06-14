from pyrannic import ServiceProvider
from app.http.middlewares.middleware_a import A_Middleware
from app.http.middlewares.middleware_b import B_Middleware


class MiddlewaresServiceProvider(ServiceProvider):
    def register(self):
        self.app.add_middleware(B_Middleware)
        self.app.add_middleware(A_Middleware)
