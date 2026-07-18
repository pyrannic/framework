from fastapi import APIRouter

from pyrannic.ioc import Resolve
from app.http.resources.hero import HeroesCollection
from app.services.heroes import HeroesServiceInterface

router = APIRouter(tags=["Heroes"])


@router.get("/heroes")
def index(service: Resolve[HeroesServiceInterface]) -> HeroesCollection:
    return HeroesCollection(service.fetch_all())
