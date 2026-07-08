from typing import Annotated, Any

from pyrannic import Resolves
from src.app.services.heroes import HeroesServiceInterface


class HeroStats:
    def generate(self, service: Annotated[HeroesServiceInterface, Resolves()]) -> Any:
        return service.fetch_stats(self.name)
