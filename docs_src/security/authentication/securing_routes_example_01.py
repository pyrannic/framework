from fastapi import APIRouter

from pyrannic.auth import Authenticate

router = APIRouter(
    tags=["Posts"],
    prefix="/posts",
    dependencies=[Authenticate()],
)
