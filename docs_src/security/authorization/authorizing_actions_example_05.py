from typing import Annotated

from app.http.requests.post import PostRequest
from app.http.resources.post import Post as PostResource
from app.repositories.posts import PostsRepository
from fastapi import APIRouter, Body

from pyrannic import ResourceNotFoundException
from pyrannic.contracts import GateInterface
from pyrannic.ioc import Resolves

router = APIRouter(tags=["Posts"], prefix="/posts")


@router.put(
    "/{post_id}",
    summary="Update a Post given its ID",
    description="Endpoint to update a post.",
)
async def update(
    post_id: int,
    request: Annotated[PostRequest, Body()],
    repository: Resolves[PostsRepository],
    gate: Resolves[GateInterface],
) -> PostResource:
    post = await repository.find(post_id)

    if post is None:
        raise ResourceNotFoundException(post_id)

    await gate.authorize("update", post)

    post.title = request.title
    post.content = request.content

    await repository.update(post)

    return PostResource.from_model(post)
