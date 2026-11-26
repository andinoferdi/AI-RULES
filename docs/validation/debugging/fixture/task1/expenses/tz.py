"""The office's business time zone. Jakarta (WIB) is UTC+7 all year."""
from datetime import timedelta, timezone

BUSINESS_TZ = timezone(timedelta(hours=7), "WIB")
