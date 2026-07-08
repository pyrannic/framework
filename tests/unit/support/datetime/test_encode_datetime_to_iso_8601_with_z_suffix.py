from datetime import datetime

from pyrannic.support.datetime import encode_datetime_to_iso_8601_with_z_suffix


def test_encode_datetime_to_iso_8601_with_z_suffix():
    """
    Test that a datetime object is correctly encoded to ISO 8601 format with 'Z' suffix.
    """

    dt = datetime(2023, 10, 5, 14, 30, 45, 123456)
    encoded = encode_datetime_to_iso_8601_with_z_suffix(dt)
    assert encoded == "2023-10-05T14:30:45.123Z"
