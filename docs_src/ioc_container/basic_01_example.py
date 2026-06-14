from typing import Annotated

from fastapi import APIRouter

from pyrannic import Resolves
from src.app.http.resources.hero import HeroesCollection
from src.app.services.heroes import HeroesServiceInterface

router = APIRouter(tags=["Heroes"])


@router.get("/heroes")
def index(service: Annotated[HeroesServiceInterface, Resolves()]) -> HeroesCollection:
    return HeroesCollection(service.fetch_all())
