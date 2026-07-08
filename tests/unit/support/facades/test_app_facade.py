from pyrannic.contracts.application import ApplicationInterface
from pyrannic.facades import App


def test_get_facade_accessor():
    assert App.facade_accessor == "app"  # pyright: ignore[reportUnknownMemberType, reportAttributeAccessIssue]


def test_get_facade_root(application: ApplicationInterface):
    assert App._get_facade_root() == application  # pyright: ignore[reportUnknownMemberType, reportAttributeAccessIssue]


def test_app_interface_properties(application: ApplicationInterface):
    assert application.container == App.container
    assert application.base_path == App.base_path
