from pytest import LogCaptureFixture

from pyrannic.contracts import ApplicationInterface
from pyrannic.facades import Log


def test_get_facade_accessor():
    assert Log.facade_accessor == "log"  # pyright: ignore[reportUnknownMemberType, reportAttributeAccessIssue]


# def test_get_facade_root(application: ApplicationInterface):
#    assert Log._get_facade_root() == application  # pyright: ignore[reportUnknownMemberType, reportAttributeAccessIssue]


def test_log_interface_properties(
    application: ApplicationInterface,
    caplog: LogCaptureFixture,
):
    # The application is pass as parameter to the test, so we can assume that the Log facade is already set up with the application instance.
    Log.info("Test log message")
    assert "Test log message" in caplog.text
