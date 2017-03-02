import uuid
from datetime import datetime, timezone

import pytest

from pb.utils import json


test_data = [
    (
        '"000102616263"',
        b'\x00\x01\x02abc'
    ),
    (
        '"2038-01-19T03:14:07+00:00"',
        datetime(2038, 1, 19, 3, 14, 7, tzinfo=timezone.utc)
    ),
    (
        '"f206ff9b-ceff-4132-b22e-d5d7e2a62708"',
        uuid.UUID('f206ff9b-ceff-4132-b22e-d5d7e2a62708')
    )
]


@pytest.fixture
def encoder():
    return json.HumanJSONEncoder()


@pytest.mark.parametrize("json_input,native", test_data)
def test_encode(encoder, json_input, native):
    assert encoder.encode(native) == json_input


def test_encode_fallback(encoder):
    class C:
        pass

    with pytest.raises(TypeError):
        encoder.encode(C)
