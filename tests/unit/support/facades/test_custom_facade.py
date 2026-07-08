from pyrannic.contracts.application import ApplicationInterface
from tests.unit.support.facades.custom_facade import CustomFacade


def test_get_facade_accessor():
    assert CustomFacade.facade_accessor == "app"  # pyright: ignore[reportUnknownMemberType, reportAttributeAccessIssue]


def test_get_facade_root(application: ApplicationInterface):
    assert CustomFacade._get_facade_root() == application  # pyright: ignore[reportUnknownMemberType, reportAttributeAccessIssue]


def test_app_interface_properties(application: ApplicationInterface):
    assert application.container == CustomFacade.container
    assert application.base_path == CustomFacade.base_path
