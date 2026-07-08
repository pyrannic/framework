from datetime import datetime, timezone

from pyrannic.support.datetime import get_current_utc_datetime


def test_get_current_utc_datetime():
    """
    Test that the get_current_utc_datetime function returns the current UTC datetime.
    """

    now = datetime.now(tz=timezone.utc)
    current_utc = get_current_utc_datetime()
    assert current_utc.tzinfo == timezone.utc
    assert abs((current_utc - now).total_seconds()) < 1
