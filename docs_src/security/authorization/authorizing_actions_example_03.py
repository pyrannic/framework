if await gate.any(["update-post", "delete-post"], post):
    # The user can update or delete the post

if await gate.none(["update-post", "delete-post"], post):
    # The user can't update or delete the post
