from app.models.post import Post

if not await guard.user.can("create", Post):
    raise ForbiddenException("User does not have permission to create a post.")
