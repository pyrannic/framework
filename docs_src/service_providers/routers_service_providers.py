from pyrannic import ServiceProvider
from app.http.routers.heroes import router as heroes_router
from app.http.routers.villains import router as villains_router


class RoutersServiceProvider(ServiceProvider):
    def register(self):
        self.app.include_router(heroes_router)
        self.app.include_router(villains_router)
