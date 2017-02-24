from datetime import timezone

from pb.utils import datetime


def test_datetime_tzinfo():
    dt = datetime.now()

    assert dt.tzinfo == timezone.utc
