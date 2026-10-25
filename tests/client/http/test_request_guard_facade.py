import asyncio

import pytest
from httpx import ASGITransport, AsyncClient
from starlette.testclient import TestClient

from pyrannic import Application
from pyrannic.auth.guards.base_guard import BaseGuard
from pyrannic.auth.safeguard import Authenticate
from pyrannic.contracts import (
    AuthenticatableInterface,
    GuardInterface,
)
from pyrannic.facades import Guard
from pyrannic.ioc import Resolves
from tests.conftest import MemoryUserProvider, User


@pytest.mark.skip(
    reason="Skipping test for concurrent request isolation of Guard facade"
)
@pytest.mark.asyncio
async def test_guard_facade_isolated_between_concurrent_requests(
    application: Application,
):
    ready = asyncio.Event()
    entered = 0

    @application.get("/guard-facade", dependencies=[Authenticate(allow_guests=True)])
    async def route() -> dict[str, str | None]:
        nonlocal entered
        entered += 1
        if entered == 2:
            ready.set()
        await asyncio.wait_for(ready.wait(), timeout=5)
        await asyncio.sleep(0)
        return {"id": Guard.maybe_id}

    provider = MemoryUserProvider()
    async with AsyncClient(
        transport=ASGITransport(app=application), base_url="http://test"
    ) as client:
        first, second = await asyncio.gather(
            client.get(
                "/guard-facade",
                headers={"Authorization": f"Bearer {provider.users[1].password}"},
            ),
            client.get(
                "/guard-facade",
                headers={"Authorization": f"Bearer {provider.users[2].password}"},
            ),
        )
        guest = await client.get("/guard-facade")

    assert first.status_code == second.status_code == guest.status_code == 200
    assert first.json() == {"id": "1"}
    assert second.json() == {"id": "2"}
    assert guest.json() == {"id": None}
    with pytest.raises(ValueError, match="No instance found"):
        _ = Guard.maybe_user


@pytest.mark.skip(reason="Skipping test for Guard facade in sync routes")
@pytest.mark.parametrize("typed", [False, True])
@pytest.mark.parametrize("scoped_guard", [False, True])
def test_guard_facade_uses_injected_guard_in_sync_route(
    application: Application, typed: bool, scoped_guard: bool
):
    if not scoped_guard:
        application.container.bind(GuardInterface[AuthenticatableInterface], BaseGuard)

    if typed:

        @application.get("/guard-facade")
        def typed_route(guard: Resolves[GuardInterface[User]]) -> str | None:
            guard.set_user(User(id=42, password=""))
            return Guard.maybe_id

    else:

        @application.get("/guard-facade")
        def route(
            guard: Resolves[GuardInterface[AuthenticatableInterface]],
        ) -> str | None:
            guard.set_user(User(id=42, password=""))
            return Guard.maybe_id

    with TestClient(application) as client:
        response = client.get("/guard-facade")
    assert response.status_code == 200
    assert response.json() == "42"
