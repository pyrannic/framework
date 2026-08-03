import pytest

from pyrannic.auth import ForbiddenException, UnauthorizedException
from pyrannic.auth.access.gate import Gate
from pyrannic.contracts.application import ApplicationInterface
from pyrannic.contracts.auth.access.gate import GateInterface
from tests.unit.auth.conftest import Order, OrderPolicy, Post


@pytest.mark.asyncio
async def test_gate_user_raises_unauthorized_exception(
    application: ApplicationInterface,
):
    gate = Gate(application.container)

    with pytest.raises(UnauthorizedException) as exc_info:
        gate.user

    error = str(exc_info.value)
    assert "401: This action is unauthorized." in error


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


def test_gate_define_ability(gate: GateInterface):
    gate.define_ability("new-ability", lambda user: user.id == 1)  # type: ignore
    assert gate.has("new-ability")
    assert gate.allows("new-ability")


def test_gate_define_policy(gate: GateInterface):
    gate.define_policy(Order, OrderPolicy)
    assert gate.allows("create", Order)
    assert gate.allows("update", Order(id=1, user_id=1))
