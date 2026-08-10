import pytest

from pyrannic.auth import ForbiddenException, UnauthorizedException
from pyrannic.auth.access.gate import Gate
from pyrannic.contracts.application import ApplicationInterface
from pyrannic.contracts.auth.access.gate import GateInterface
from tests.conftest import (
    Category,
    Order,
    OrderPolicy,
    Post,
    PostEntity,
    PostModel,
    PostPolicy,
    PostSchema,
    PostTable,
    User,
)


def test_gate_user_raises_unauthorized_exception(
    application: ApplicationInterface,
):
    gate = Gate(application.container)

    with pytest.raises(UnauthorizedException) as exc_info:
        gate.user

    error = str(exc_info.value)
    assert "401: This action is unauthorized." in error


def test_gate_user(gate: GateInterface):
    user = User(id=1, password="password")
    gate.set_user(user)
    assert gate.user == user


def test_gate_has(gate: GateInterface):
    assert gate.has("create-post")
    assert gate.has("update-post", "delete-post")
    assert not gate.has("non-existent-ability")


@pytest.mark.asyncio
async def test_gate_allows_with_abilities(gate: GateInterface):
    assert await gate.allows("create-post")
    assert await gate.allows(["update-post", "delete-post"], Post(id=1, user_id=1))
    assert not await gate.allows("non-existent-ability")


@pytest.mark.asyncio
async def test_gate_allows_with_policies(gate: GateInterface):
    assert await gate.allows("create", Post)
    assert await gate.allows(["update", "delete"], Post(id=1, user_id=1))
    assert not await gate.allows("non-existent-ability", Post)


@pytest.mark.asyncio
async def test_gate_denies_with_abilities(gate: GateInterface):
    assert await gate.denies("update-post", Post(id=1, user_id=2))
    assert await gate.denies(["update-post", "delete-post"], Post(id=1, user_id=2))
    assert await gate.denies("non-existent-ability")


@pytest.mark.asyncio
async def test_gate_denies_with_policies(gate: GateInterface):
    assert await gate.denies("update", Post(id=1, user_id=2))
    assert await gate.denies(["update", "delete"], Post(id=1, user_id=2))
    assert await gate.denies("non-existent-ability", Post)


@pytest.mark.asyncio
async def test_gate_check_with_abilities(gate: GateInterface):
    assert await gate.check("create-post")
    assert await gate.check(["update-post", "delete-post"], Post(id=1, user_id=1))
    assert not await gate.check("non-existent-ability")

    assert not await gate.check("update-post", Post(id=1, user_id=2))
    assert not await gate.check(["update-post", "delete-post"], Post(id=1, user_id=2))
    assert not await gate.check("non-existent-ability")


@pytest.mark.asyncio
async def test_gate_check_with_policies(gate: GateInterface):
    assert await gate.check("create", Post)
    assert await gate.check(["update", "delete"], Post(id=1, user_id=1))
    assert not await gate.check("non-existent-ability", Post)

    assert not await gate.check("update", Post(id=1, user_id=2))
    assert not await gate.check(["update", "delete"], Post(id=1, user_id=2))
    assert not await gate.check("non-existent-ability", Post)


@pytest.mark.asyncio
async def test_gate_any_with_abilities(gate: GateInterface):
    assert await gate.any("create-post")
    assert await gate.any(
        ["update-post", "delete-post", "non-existent-ability"],
        Post(id=1, user_id=1),
    )


@pytest.mark.asyncio
async def test_gate_any_with_policies(gate: GateInterface):
    assert await gate.any("create", Post)
    assert await gate.any(
        ["update", "delete", "non-existent-ability"],
        Post(id=1, user_id=1),
    )


@pytest.mark.asyncio
async def test_gate_none_with_abilities(gate: GateInterface):
    assert await gate.none("delete-post", Post(id=1, user_id=2))
    assert await gate.none(["update-post", "delete-post"], Post(id=1, user_id=2))


@pytest.mark.asyncio
async def test_gate_none_with_policies(gate: GateInterface):
    assert await gate.none("delete", Post(id=1, user_id=2))
    assert await gate.none(["update", "delete"], Post(id=1, user_id=2))


@pytest.mark.asyncio
async def test_gate_authorize_with_ability(gate: GateInterface):
    assert await gate.authorize("create-post")
    assert await gate.authorize("update-post", Post(id=1, user_id=1))


@pytest.mark.asyncio
async def test_gate_authorize_with_policy(gate: GateInterface):
    assert await gate.authorize("create", Post)
    assert await gate.authorize("update", Post(id=1, user_id=1))


@pytest.mark.asyncio
async def test_gate_authorize_raises_forbidden_exception_with_ability(
    gate: GateInterface,
):
    with pytest.raises(ForbiddenException) as exc_info:
        await gate.authorize("update-post", Post(id=1, user_id=2))

    error = str(exc_info.value)
    assert "403: This action is forbidden." in error


@pytest.mark.asyncio
async def test_gate_authorize_raises_forbidden_exception_with_policy(
    gate: GateInterface,
):
    with pytest.raises(ForbiddenException) as exc_info:
        await gate.authorize("update", Post(id=1, user_id=2))

    error = str(exc_info.value)
    assert "403: This action is forbidden." in error


@pytest.mark.asyncio
async def test_gate_define_ability(gate: GateInterface):
    gate.define_ability("new-ability", lambda user: user.id == 1)  # type: ignore
    assert gate.has("new-ability")
    assert await gate.allows("new-ability")


@pytest.mark.asyncio
async def test_gate_define_policy(gate: GateInterface):
    gate.define_policy(Order, OrderPolicy)
    assert await gate.allows("create", Order)
    assert await gate.allows("update", Order(id=1, user_id=1))


@pytest.mark.asyncio
async def test_gate_policy_with_resource_as_str(gate: GateInterface):
    assert await gate.allows("create", "Post")


@pytest.mark.asyncio
async def test_gate_with_resource_with_suffixes(gate: GateInterface):
    gate.define_policy(PostTable, PostPolicy)
    gate.define_policy(PostModel, PostPolicy)
    gate.define_policy(PostEntity, PostPolicy)
    gate.define_policy(PostSchema, PostPolicy)

    assert await gate.allows("update", PostTable(id=1, user_id=1))
    assert await gate.allows("update", PostModel(id=1, user_id=1))
    assert await gate.allows("update", PostEntity(id=1, user_id=1))
    assert await gate.allows("update", PostSchema(id=1, user_id=1))


@pytest.mark.asyncio
async def test_gate_with_different_policy_formats(gate: GateInterface):
    assert await gate.allows("mark_as_read", Post(id=1, user_id=2))
    assert await gate.allows("Mark_As_Read", Post(id=1, user_id=2))
    assert await gate.allows("MARK_AS_READ", Post(id=1, user_id=2))

    assert await gate.allows("mark-as-read", Post(id=1, user_id=2))
    assert await gate.allows("Mark-As-Read", Post(id=1, user_id=2))
    assert await gate.allows("MARK-AS-READ", Post(id=1, user_id=2))

    assert await gate.allows("markAsRead", Post(id=1, user_id=2))
    assert await gate.allows("MarkAsRead", Post(id=1, user_id=2))


@pytest.mark.asyncio
async def test_gate_with_policy_returning_response(gate: GateInterface):
    assert await gate.allows("mark_as_read", Post(id=1, user_id=2))


@pytest.mark.asyncio
async def test_gate_with_policy_raising_unauthorized_exception(gate: GateInterface):
    assert await gate.denies("rate", Post(id=1, user_id=2))


@pytest.mark.asyncio
async def test_gate_with_async_policy(gate: GateInterface):
    gate.define_policy(Order, OrderPolicy)
    assert await gate.allows("archive", Order(id=1, user_id=1))


@pytest.mark.asyncio
async def test_gate_guess_policy_names_using(gate: GateInterface):
    gate.guess_policy_names_using(
        lambda resource: Category.__module__ + ".CategoryPolicy"
    )
    assert await gate.allows("remove", Category(id=1, user_id=1))


@pytest.mark.asyncio
async def test_gate_resource_doesnt_exist_denies_always(gate: GateInterface):
    assert await gate.denies("add", "Tag")
    assert not await gate.allows("add", "Tag")


@pytest.mark.asyncio
async def test_gate_before_method_returns_false(gate: GateInterface):
    assert await gate.for_user(User(id=1, password="password", is_banned=True)).denies(
        "publish", Post(id=1, user_id=1)
    )


@pytest.mark.asyncio
async def test_gate_before_method_returns_true(gate: GateInterface):
    assert await gate.for_user(User(id=1, password="password", is_admin=True)).allows(
        "rate", Post(id=1, user_id=1)
    )


@pytest.mark.asyncio
async def test_gate_async_before_method(gate: GateInterface):
    gate.define_policy(Order, OrderPolicy)
    assert await gate.for_user(User(id=1, password="password", is_admin=True)).allows(
        "delete", Order(id=1, user_id=1)
    )


@pytest.mark.asyncio
async def test_gate_with_guest_user(gate: GateInterface):
    # Configure the gate as unauthenticated (a.k.a. guest user)
    gate = gate.set_user(None)
    assert await gate.allows("rate", Post(id=1, user_id=1))
