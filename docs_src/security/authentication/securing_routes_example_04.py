from app.models.user import User

from pyrannic.auth import Authenticate
from pyrannic.contracts import GuardInterface
from pyrannic.ioc import Resolves


@router.get(
    "/posts",
    summary="Posts Endpoint",
    description="Endpoint to retrieve the list of posts.",
    dependencies=[Authenticate(allow_guests=True)],
)
async def index(guard: Resolves[GuardInterface[User]]):
    if guard.check:
        # The user is logged in...
    else:
        # The user is a guest...
