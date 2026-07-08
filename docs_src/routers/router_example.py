from typing import Annotated

from fastapi import APIRouter, Depends

from app.http.resources.hero import HeroesCollection
from app.repositories.heroes import HeroesRepository

router = APIRouter(tags=["Heroes"])


@router.get("/heroes")
def index(repository: Annotated[HeroesRepository, Depends()]) -> HeroesCollection:
    return HeroesCollection(repository.paginate())
