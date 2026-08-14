from app.models import Post, User


class PostPolicy:
    def update(self, user: User, post: Post, category: int) -> bool:
        return user.id == post.user_id and user.can_update_category(category)
