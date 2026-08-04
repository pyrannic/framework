import os
from typing import Any, cast

import pytest
import pytest_asyncio

from pyrannic.application import Application
from pyrannic.auth.access.authorizable import Authorizable
from pyrannic.auth.access.gate import Gate, GateInterface
from pyrannic.auth.access.response import Response
from pyrannic.auth.authenticatable import Authenticatable
from pyrannic.auth.bearer_guard import BearerGuard
from pyrannic.auth.unauthorized_exception import UnauthorizedException
from pyrannic.contracts import (
    ApplicationInterface,
    AuthenticatableInterface,
    GuardInterface,
    UserProviderInterface,
)


class User(Authenticatable, Authorizable):
    def __init__(self, id: int, password: str):
        self.id = id
        self.password = password


class Post:
    def __init__(self, id: int, user_id: int):
        self.id = id
        self.user_id = user_id


class PostTable(Post):
    pass


class PostModel(Post):
    pass


class PostEntity(Post):
    pass


class PostSchema(Post):
    pass


class Order:
    def __init__(self, id: int, user_id: int):
        self.id = id
        self.user_id = user_id


class Category:
    def __init__(self, id: int, user_id: int):
        self.id = id
        self.user_id = user_id


class PostPolicy:
    def create(self, user: User) -> bool:
        return True

    def show(self, user: User, post: Post | None = None) -> bool:
        return True

    def update(self, user: User, post: Post) -> bool:
        return user.id == post.user_id

    def delete(self, user: User, post: Post) -> bool:
        return user.id == post.user_id

    def mark_as_read(self, user: User, post: Post) -> Response:
        return (
            Response.allow()
            if user.id != post.user_id
            else Response.deny("You cannot mark this post as read.")
        )

    def rate(self, user: User, post: Post) -> Response:
        raise UnauthorizedException(
            "You cannot rate this post because you are not authorized to do so."
        )


class OrderPolicy:
    def create(self, user: User) -> bool:
        return True

    def show(self, user: User, order: Order | None = None) -> bool:
        return True

    def update(self, user: User, order: Order) -> bool:
        return user.id == order.user_id

    def delete(self, user: User, order: Order) -> bool:
        return user.id == order.user_id


class CategoryPolicy:
    def remove(self, user: User, category: Category) -> bool:
        return user.id == category.user_id


class MemoryUserProvider(UserProviderInterface):
    def __init__(self) -> None:
        self.users: dict[int, User] = {
            1: User(id=1, password="secret"),
            2: User(id=2, password="password"),
        }

    async def retrieve_by_id(self, identifier: Any) -> AuthenticatableInterface | None:
        return self.users.get(identifier)

    async def retrieve_by_credentials(
        self,
        *args: Any,
        **kwargs: Any,
    ) -> AuthenticatableInterface | None:
        token = kwargs.get("token")

        for user in self.users.values():
            if user.password == token:
                return user

        return None

    def validate_credentials(
        self,
        user: AuthenticatableInterface,
        credentials: dict[str, Any],
    ) -> bool:
        # Implement credential validation if needed
        return False


async def setup_auth(
    application: ApplicationInterface,
) -> tuple[GateInterface, GuardInterface[User], MemoryUserProvider]:
    gate = Gate(
        application.container,
        abilities={
            "show-post": lambda _: True,  # type: ignore
            "rate-post": lambda _: True,  # type: ignore
            "create-post": lambda _: True,  # type: ignore
            "update-post": lambda user, post: user.id == post.user_id,  # type: ignore
            "delete-post": lambda user, post: user.id == post.user_id,  # type: ignore
        },
        policies={
            Post.__name__: PostPolicy,
        },
    )
    provider = MemoryUserProvider()
    guard = BearerGuard(provider)

    user = await provider.retrieve_by_id(1)

    if user:
        guard.set_user(user)
        gate.set_user(cast(Authorizable, user))

    application.container.instance(GateInterface, gate)
    application.container.instance(GuardInterface[User], guard)
    application.container.instance(UserProviderInterface, provider)

    return gate, cast(GuardInterface[User], guard), provider


@pytest.fixture(scope="module")
def application() -> ApplicationInterface:
    return Application(base_path="tests/application")


@pytest.fixture(scope="session", autouse=True)
def set_env():
    os.environ["DB_DATABASE"] = ":memory:"


@pytest_asyncio.fixture(scope="module")
async def guard(application: ApplicationInterface) -> GuardInterface[User]:
    (_, guard, __) = await setup_auth(application)
    return guard


@pytest_asyncio.fixture(scope="function")
async def gate(application: ApplicationInterface) -> GateInterface:
    (gate, _, __) = await setup_auth(application)
    return gate
