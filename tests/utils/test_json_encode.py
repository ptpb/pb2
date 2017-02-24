from datetime import datetime, timezone
import uuid

import pytest

from pb.utils import json as _json


@pytest.fixture
def json():
    return _json.JSONEncoder()


@pytest.mark.parametrize("json_input,native", [
    (
        '{"__bytes__": true, "hex": "000102616263"}',
        b'\x00\x01\x02abc'
    ),
    (
        '{"__datetime__": true, "timestamp": 2147483647.0}',
        datetime(2038, 1, 19, 3, 14, 7, tzinfo=timezone.utc)
    ),
    (
        '{"__uuid__": true, "hex": "f206ff9bceff4132b22ed5d7e2a62708"}',
        uuid.UUID('f206ff9b-ceff-4132-b22e-d5d7e2a62708')
    )
])
def test_encode(json, json_input, native):
    assert json.encode(native) == json_input


def test_encode_fallback(json):
    class C:
        pass

    with pytest.raises(TypeError):
        json.encode(C)
