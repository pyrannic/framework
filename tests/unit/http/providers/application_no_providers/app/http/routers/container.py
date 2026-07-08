from fastapi import APIRouter

from pyrannic.ioc import Resolve

from tests.application.app.repositories.heroes import (
    HeroesRepository,
    HeroesScopedRepository,
    HeroesSingletonRepository,
)


router = APIRouter(tags=["Container Routes"])


@router.get(
    "/object_memory_address",
    summary="Object Memory Address Endpoint",
    description="Endpoint to retrieve the memory address of the object.",
)
def get_object_memory_address(repository: Resolve[HeroesRepository]) -> str:
    return hex(id(repository))


@router.get(
    "/scoped_memory_address",
    summary="Scoped Memory Address Endpoint",
    description="Endpoint to retrieve the memory address of the scoped object.",
)
def get_scoped_memory_address(repository: Resolve[HeroesScopedRepository]) -> str:
    return hex(id(repository))


@router.get(
    "/singleton_memory_address",
    summary="Singleton Memory Address Endpoint",
    description="Endpoint to retrieve the memory address of the singleton object.",
)
def get_singleton_memory_address(repository: Resolve[HeroesSingletonRepository]) -> str:
    return hex(id(repository))
