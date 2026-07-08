from datetime import datetime, timezone

from pyrannic.support.datetime import get_endday_utc_datetime


def test_get_endday_utc_datetime():
    """
    Test that the get_endday_utc_datetime function returns the end of the current UTC day.
    """

    now = datetime.now(tz=timezone.utc)
    endday_utc = get_endday_utc_datetime()
    assert endday_utc.tzinfo == timezone.utc
    assert endday_utc.date() == now.date()
    assert endday_utc.hour == 23
    assert endday_utc.minute == 59
    assert endday_utc.second == 59
    assert endday_utc.microsecond == 999999
