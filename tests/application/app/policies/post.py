from tests.application.app.models.post import Post
from tests.application.app.models.user import User


class PostPolicy:
    def before(self, ability: str, user: User, post: Post | None = None) -> bool | None:
        return False

    def create(self, user: User) -> bool:
        return True

    def show(self, user: User, post: Post | None = None) -> bool:
        return True

    def update(self, user: User, post: Post) -> bool:
        return user.id == post.user_id

    def delete(self, user: User, post: Post) -> bool:
        return user.id == post.user_id
