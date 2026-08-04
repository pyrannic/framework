from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends

from pyrannic import ResourceNotFoundException
from pyrannic.auth import Authenticate
from pyrannic import ResourceNotFoundException, Safeguard
from pyrannic.contracts import GateInterface, GuardInterface
from pyrannic.ioc import Resolves
from tests.application.app.http.resources.hero import Hero, HeroesCollection
from tests.application.app.models.hero import Hero as HeroModel
from tests.application.app.models.user import User
from tests.application.app.repositories.heroes import HeroesRepository

router = APIRouter(
    tags=["Heroes"],
    dependencies=[Authenticate()],
)


@router.get(
    "/heroes",
    summary="Heroes Endpoint",
    description="Endpoint to retrieve the list of heroes.",
)
async def index(
    # container: Resolves[ContainerInterface],
    # container2: Container,
    # app: App,
    # repository3: Resolves[HeroesRepository],
    # repository4: Resolves[HeroesRepository],
    # foo: Resolves[FooServiceInterface],
    # bar: Resolves[BarService],
    guard: Resolves[GuardInterface[User]],
    gate: Resolves[GateInterface],
    repository: HeroesRepository = Depends(),
    # repository: Scoped[Repository[HeroModel]],
) -> HeroesCollection:
    print(f"Guard: {guard.user.email}")

    if await gate.user.can("create", HeroModel):
        print("User can create heroes!!!")

    if await gate.user.can("view", HeroModel()):
        print("User can view heroes!!!")

    return HeroesCollection(repository.paginate())
    # return HeroesCollection(repository.where(HeroModel.name.like("%man%")).paginate())


@router.get(
    "/heroes_empty_collection",
    summary="Heroes Empty Collection Endpoint",
    description="Endpoint to retrieve an empty collection of heroes.",
)
def empty_collection() -> HeroesCollection:
    return HeroesCollection([])


@router.get(
    "/heroes_static_collection",
    summary="Heroes Static Collection Endpoint",
    description="Endpoint to retrieve a static collection of heroes.",
)
def static_collection() -> HeroesCollection:
    now = datetime.now()

    return HeroesCollection(
        [
            Hero(
                id="superman",
                name="Superman",
                description="The Man of Steel",
                created_at=now,
                updated_at=now,
            )
        ]
    )


@router.get(
    "/heroes/{hero_id}",
    summary="Get Hero Endpoint",
    description="Endpoint to retrieve a specific hero by ID.",
)
def show(
    hero_id: str,
    repository: Annotated[HeroesRepository, Depends()],
) -> Hero:
    hero = repository.find(hero_id)

    if not hero:
        raise ResourceNotFoundException(hero_id)

    return Hero.from_model(hero)


@router.delete(
    "/heroes/{hero_id}",
    summary="Delete Hero Endpoint",
    description="Endpoint to delete a specific hero by ID.",
    status_code=204,
)
def destroy(
    hero_id: str,
    repository: Annotated[HeroesRepository, Depends()],
) -> None:
    hero = repository.find(hero_id)

    if not hero:
        raise ResourceNotFoundException(hero_id)

    repository.remove(hero)


@router.patch(
    "/heroes/{hero_id}/restore",
    summary="Restore Hero Endpoint",
    description="Endpoint to restore a specific hero by ID.",
)
def restore(
    hero_id: str,
    repository: Annotated[HeroesRepository, Depends()],
) -> Hero:
    hero = repository.with_removed().find(hero_id)

    if not hero:
        raise ResourceNotFoundException(hero_id)

    return Hero.from_model(repository.restore(hero))


@router.post(
    "/heroes",
    summary="Create Hero Endpoint",
    description="Endpoint to create a new hero.",
)
def create(repository: Annotated[HeroesRepository, Depends()]) -> Hero:
    return Hero.from_model(
        repository.create(
            HeroModel(
                name="Superman",
                description="The Man of Steel",
            )
        )
    )
