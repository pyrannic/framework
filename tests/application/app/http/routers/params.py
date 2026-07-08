from fastapi import APIRouter

from pyrannic.ioc import Scoped, Singleton, Resolve
from tests.application.app.repositories.heroes import (
    HeroesRepository,
    HeroesRepository2,
    HeroesRepository3,
)

router = APIRouter(tags=["Params Routes"])


@router.get(
    "/params/resolve_memory_address",
    summary="Resolve Memory Address Endpoint",
    description="Endpoint to retrieve the memory address of the resolved object.",
)
def get_resolve_memory_address(
    repository: Resolve[HeroesRepository],
    repository2: Resolve[HeroesRepository],
) -> tuple[str, str]:
    return (hex(id(repository)), hex(id(repository2)))


@router.get(
    "/params/scoped_memory_address",
    summary="Scoped Memory Address Endpoint",
    description="Endpoint to retrieve the memory address of the scoped object.",
)
def get_scoped_memory_address(
    repository: Scoped[HeroesRepository2],
    repository2: Scoped[HeroesRepository2],
) -> tuple[str, str]:
    return (hex(id(repository)), hex(id(repository2)))


@router.get(
    "/params/singleton_memory_address",
    summary="Singleton Memory Address Endpoint",
    description="Endpoint to retrieve the memory address of the singleton object.",
)
def get_singleton_memory_address(
    repository: Singleton[HeroesRepository3],
    repository2: Singleton[HeroesRepository3],
) -> tuple[str, str]:
    return (hex(id(repository)), hex(id(repository2)))
