from fastapi import APIRouter

from pyrannic.facades import App


router = APIRouter(tags=["Facade Routes"])


@router.get(
    "/app_base_path",
    summary="App Base Path Endpoint",
    description="Endpoint to retrieve the app base path.",
)
def get_app_base_path() -> str:
    return App.base_path
