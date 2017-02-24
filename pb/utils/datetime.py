from datetime import datetime, timezone


def now():
    dt = datetime.utcnow()
    dt = dt.replace(tzinfo=timezone.utc)

    return dt
