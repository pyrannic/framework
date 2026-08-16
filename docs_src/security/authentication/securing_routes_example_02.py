from pyrannic.auth import Authenticate


@router.get(
    "/posts",
    summary="Posts Endpoint",
    description="Endpoint to retrieve the list of posts.",
    dependencies=[Authenticate()],
)
async def index():
    pass
