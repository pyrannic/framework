from fastapi import APIRouter

from tests.application.app.http.routers.heroes import router as heroes_router
from tests.application.app.http.routers.container import (
    router as container_router,
)


routers: list[APIRouter] = [
    container_router,
    heroes_router,
]
