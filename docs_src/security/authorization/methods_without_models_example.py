def create(self, user: User) -> bool:
    """Determine if the given user can create posts."""
    return user.role == "writer"
