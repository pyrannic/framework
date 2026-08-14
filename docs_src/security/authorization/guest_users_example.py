from app.models import Post, User


class PostPolicy:
    def update(self, user: User | None, post: Post) -> bool:
        """Determine if the given post can be updated by the user."""
        return user is not None and user.id == post.user_id
