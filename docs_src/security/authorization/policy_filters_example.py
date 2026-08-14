from app.models import User


class PostPolicy:
    def before(self, ability: str, user: User) -> bool | None:
        if user.is_administrator:
            return True

        return None
