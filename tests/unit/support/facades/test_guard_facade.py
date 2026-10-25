from pyrannic.contracts import AuthenticatableInterface
from pyrannic.contracts.auth.guard import GuardInterface
from pyrannic.facades import Guard  # pyright: ignore[reportUnknownVariableType]
from tests.conftest import User


def test_get_facade_accessor():
    assert Guard.facade_accessor == GuardInterface[AuthenticatableInterface]


def test_get_facade_root(guard: GuardInterface[User]):
    assert Guard._get_facade_root() == guard  # pyright: ignore[reportCallIssue, reportPrivateUsage, reportAttributeAccessIssue, reportUnknownMemberType]


def test_guard_facade_interface_properties(guard: GuardInterface[User]):
    assert Guard.maybe_id == "1"
