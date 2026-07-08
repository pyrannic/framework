from datetime import datetime, timedelta, timezone


def get_current_utc_datetime() -> datetime:
    return datetime.now(tz=timezone.utc)


def get_today_utc_datetime() -> datetime:
    return get_current_utc_datetime().replace(hour=0, minute=0, second=0, microsecond=0)


def get_endday_utc_datetime() -> datetime:
    return get_today_utc_datetime() + timedelta(days=1) - timedelta(microseconds=1)


def encode_datetime_to_iso_8601_with_z_suffix(date: datetime) -> str:
    return date.replace(tzinfo=None).isoformat(sep="T", timespec="milliseconds") + "Z"
