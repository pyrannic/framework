if await gate.allows("update", post):
    # The user can update the post

if await gate.denies("update", post):
    # The user can't update the post
