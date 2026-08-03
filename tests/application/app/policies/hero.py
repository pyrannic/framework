from tests.application.app.models.hero import Hero
from tests.application.app.models.user import User


class HeroPolicy:
    def create(self, user: User) -> bool:
        return True

    def view(self, user: User, hero: Hero) -> bool:
        return True

    def update(self, user: User, hero: Hero) -> bool:
        return False
