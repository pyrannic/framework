from typing import Annotated

from app.http.requests.post import PostRequest
from app.http.resources.post import Post as PostResource
from app.models.user import User
from app.repositories.posts import PostsRepository
from fastapi import APIRouter, Body

from pyrannic import ForbiddenException, ResourceNotFoundException
from pyrannic.contracts import GuardInterface
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
    guard: Resolves[GuardInterface[User]],
) -> PostResource:
    post = await repository.find(post_id)

    if post is None:
        raise ResourceNotFoundException(post_id)

    if not await guard.user.can("update", post):
        raise ForbiddenException("User does not have permission to update this post.")

    post.title = request.title
    post.content = request.content

    await repository.update(post)

    return PostResource.from_model(post)
