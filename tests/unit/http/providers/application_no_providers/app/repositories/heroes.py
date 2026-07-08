from pyrannic.container.decorators import scoped, singleton
from pyrannic.orm.sqlalchemy.repository import Repository
from tests.application.app.models.hero import Hero


class HeroesRepository(Repository[Hero]):
    pass


@scoped
class HeroesScopedRepository(Repository[Hero]):
    pass


@singleton
class HeroesSingletonRepository(Repository[Hero]):
    pass
