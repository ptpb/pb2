import uuid
from datetime import datetime, timezone

import pytest

from pb.utils import json


test_data = [
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
]


@pytest.fixture
def encoder():
    return json.JSONEncoder(sort_keys=True)


@pytest.fixture
def decoder():
    return json.JSONDecoder()


@pytest.mark.parametrize("json_input,native", test_data)
def test_encode(encoder, json_input, native):
    assert encoder.encode(native) == json_input


@pytest.mark.parametrize("json_input,native", test_data)
def test_decode(decoder, json_input, native):
    assert decoder.decode(json_input) == native


def test_encode_fallback(encoder):
    class C:
        pass

    with pytest.raises(TypeError):
        encoder.encode(C)


def test_decode_fallback(decoder):
    assert decoder.decode("{}") == {}
