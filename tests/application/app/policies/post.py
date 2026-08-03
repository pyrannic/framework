from tests.application.app.models.post import Post
from tests.application.app.models.user import User


class PostPolicy:
    def create(self, user: User) -> bool:
        return True

    def show(self, user: User, post: Post | None = None) -> bool:
        return True

    def update(self, user: User, post: Post) -> bool:
        return user.id == post.user_id

    def delete(self, user: User, post: Post) -> bool:
        return user.id == post.user_id
