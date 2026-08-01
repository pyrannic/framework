from tests.application.app.models.hero import Hero
from tests.application.app.models.user import User


class HeroPolicy:
    def create(self, user: User) -> bool:
        print(f"User: {user}")
        return True

    def view(self, user: User, hero: Hero) -> bool:
        print(f"User: {user}")
        print(f"Hero: {hero}")
        return True

    def update(self, user: User, hero: Hero) -> bool:
        print(f"User: {user}")
        print(f"Hero: {hero}")
        return False
