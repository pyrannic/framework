import pytest

from pyrannic.contracts.auth.guard import GuardInterface
from tests.conftest import Post, User


@pytest.mark.asyncio
async def test_authorizable_cannot_ability(guard: GuardInterface[User]):
    assert await guard.user.cannot("update-post", Post(id=1, user_id=2))


@pytest.mark.asyncio
async def test_authorizable_cannot_abilities(guard: GuardInterface[User]):
    assert await guard.user.cannot(
        ["delete-post", "update-post"], Post(id=1, user_id=2)
    )


@pytest.mark.asyncio
async def test_authorizable_cant_ability(guard: GuardInterface[User]):
    assert await guard.user.cant("update-post", Post(id=1, user_id=2))


@pytest.mark.asyncio
async def test_authorizable_cant_abilities(guard: GuardInterface[User]):
    assert await guard.user.cant(["update-post", "delete-post"], Post(id=1, user_id=2))


@pytest.mark.asyncio
async def test_authorizable_can_ability(guard: GuardInterface[User]):
    assert await guard.user.can("show-post", Post)


@pytest.mark.asyncio
async def test_authorizable_can_abilities(guard: GuardInterface[User]):
    assert await guard.user.can(["show-post", "rate-post"], Post)


@pytest.mark.asyncio
async def test_authorizable_can_any_abilities(guard: GuardInterface[User]):
    assert await guard.user.can_any(["show-post", "delete-post"], Post)


@pytest.mark.asyncio
async def test_authorizable_cannot_policy(guard: GuardInterface[User]):
    assert await guard.user.cannot("delete", Post(id=1, user_id=2))


@pytest.mark.asyncio
async def test_authorizable_cannot_policies(guard: GuardInterface[User]):
    assert await guard.user.cannot(
        ["update", "delete"],
        Post(id=1, user_id=2),
    )


@pytest.mark.asyncio
async def test_authorizable_cant_policy(guard: GuardInterface[User]):
    assert await guard.user.cant("update", Post(id=1, user_id=2))


@pytest.mark.asyncio
async def test_authorizable_cant_policies(guard: GuardInterface[User]):
    assert await guard.user.cant(
        ["update", "delete"],
        Post(id=1, user_id=2),
    )


@pytest.mark.asyncio
async def test_authorizable_can_policy(guard: GuardInterface[User]):
    assert await guard.user.can("show", Post(id=1, user_id=1))


@pytest.mark.asyncio
async def test_authorizable_can_policies(guard: GuardInterface[User]):
    assert await guard.user.can(
        ["show", "update", "delete"],
        Post(id=1, user_id=1),
    )


@pytest.mark.asyncio
async def test_authorizable_can_any_policies(guard: GuardInterface[User]):
    assert await guard.user.can_any(["show", "delete"], Post(id=1, user_id=1))
