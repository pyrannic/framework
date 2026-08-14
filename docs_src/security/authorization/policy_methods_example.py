from app.models import Post, User


class PostPolicy:
    def update(self, user: User, post: Post) -> bool:
        """Determine if the given post can be updated by the user."""
        return user.id == post.user_id
