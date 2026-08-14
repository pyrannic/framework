async def update(
    post_id: int,
    request: Annotated[PostRequest, Body()],
    repository: Resolves[PostsRepository],
    gate: Resolves[GateInterface],
) -> PostResource:
    post = await repository.find(post_id)

    if post is None:
        raise ResourceNotFoundException(post_id)

    await gate.authorize("update", post, request.category)

    # The authenticated user can update the post

    return PostResource.from_model(post)
