from datetime import datetime
from datetime import timezone


def now():
    dt = datetime.utcnow()
    dt.replace(tzinfo=timezone.utc)

    return dt
