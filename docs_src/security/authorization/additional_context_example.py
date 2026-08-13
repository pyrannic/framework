def can_create_post(user, category, pinned):
    return user.can_publish_to_group(category.group) and (not pinned or user.can_pin_posts())

gate.define_ability("create-post", can_create_post)

if await gate.check("create-post", category, pinned):
    # The user can create the post