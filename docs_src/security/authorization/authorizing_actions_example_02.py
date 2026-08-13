if await gate.for_user(user).allows("update-post", post):
    # The user can update the post

if await gate.for_user(user).denies("update-post", post):
    # The user can't update the post
