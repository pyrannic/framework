from app.http.resources.post import PostsCollection
from app.models.user import User
from app.repositories.posts import PostsRepository
from fastapi import APIRouter

from pyrannic.contracts import GuardInterface
from pyrannic.ioc import Resolves

router = APIRouter(tags=["Posts"], prefix="/posts")


@router.get("", summary="Retrieve a list of posts")
async def index(
    repository: Resolves[PostsRepository],
    guard: Resolves[GuardInterface[User]],
) -> PostsCollection:
    # Retrieve the currently authenticated user
    user = guard.user

    # ... perform some logic with the authenticated user

    return await PostsCollection(repository.paginate())
