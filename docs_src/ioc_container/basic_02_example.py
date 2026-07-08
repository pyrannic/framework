from typing import Annotated

from fastapi import APIRouter

from pyrannic.ioc import Resolve
from src.app.http.resources.hero import HeroesCollection
from src.app.services.heroes import HeroesServiceInterface

router = APIRouter(tags=["Heroes"])


@router.get("/heroes")
def index(service: Resolve[HeroesServiceInterface]) -> HeroesCollection:
    return HeroesCollection(service.fetch_all())
