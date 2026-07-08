from datetime import datetime, timezone

from pyrannic.support.datetime import get_today_utc_datetime


def test_get_today_utc_datetime():
    """
    Test that the get_today_utc_datetime function returns the current UTC date.
    """

    now = datetime.now(tz=timezone.utc)
    today_utc = get_today_utc_datetime()
    assert today_utc.tzinfo == timezone.utc
    assert today_utc.date() == now.date()
    assert today_utc.hour == 0
    assert today_utc.minute == 0
    assert today_utc.second == 0
    assert today_utc.microsecond == 0
