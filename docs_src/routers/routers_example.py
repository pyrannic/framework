from fastapi import APIRouter

from app.http.routers.heroes import router as heroes_router
from app.http.routers.villains import router as villains_router


routers: list[APIRouter] = [
    villains_router,
    heroes_router,
]

__all__ = ["routers"]
