from fastapi import APIRouter

from tests.application.app.http.routers.container import (
    router as container_router,
)
from tests.application.app.http.routers.exceptions import router as exceptions_router
from tests.application.app.http.routers.facade import router as facade_router
from tests.application.app.http.routers.heroes import router as heroes_router
from tests.application.app.http.routers.params import router as params_router
from tests.application.app.http.routers.posts import router as posts_router
from tests.application.app.http.routers.users import router as users_router

routers: list[APIRouter] = [
    container_router,
    exceptions_router,
    facade_router,
    params_router,
    posts_router,
    users_router,
    heroes_router,
]

__all__ = ["routers"]
