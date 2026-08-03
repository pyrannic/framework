import hashlib
import os

from fastapi import APIRouter

from pyrannic.ioc import Resolves
from tests.application.app.http.resources.user import User, UsersCollection
from tests.application.app.models.user import User as UserModel
from tests.application.app.repositories.users import UsersRepository

router = APIRouter(tags=["users"], prefix="/users")


@router.get(
    "/",
    summary="Users Endpoint",
    description="Endpoint to retrieve the list of users.",
)
def index(repository: Resolves[UsersRepository]) -> UsersCollection:
    return UsersCollection(repository.paginate())


@router.post(
    "/",
    summary="Create User Endpoint",
    description="Endpoint to create a new user.",
)
def create(name: str, email: str, repository: Resolves[UsersRepository]) -> User:
    return User.from_model(
        repository.create(
            UserModel(
                name=name,
                email=email,
                password=hashlib.scrypt(
                    b"securepassword",
                    salt=os.urandom(32),
                    n=16384,
                    r=8,
                    p=1,
                ),
            )
        )
    )
