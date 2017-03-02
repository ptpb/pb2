import json
from unittest.mock import ANY

from aiohttp import multipart
from asynctest import patch

from pb.models.object import Object
from pb.storage.base import BaseStorage


@patch.object(BaseStorage, 'create_object', return_value=Object(uuid=None))
async def test_object_post(mock_create_object, cli):
    with multipart.MultipartWriter() as writer:
        writer.append('test')

    res = await cli.post('/objects', data=writer, headers=writer.headers)
    assert res.status == 200

    obj = json.loads(await res.text())

    assert isinstance(obj, list)
    assert len(obj) == 1
    assert obj[0]['uuid'] is None

    assert mock_create_object.call_count == 1


@patch.object(BaseStorage, 'read_object')
async def test_object_get(mock_read_object, cli):
    await cli.get('/object/foo')

    assert mock_read_object.call_count == 1
    mock_read_object.assert_called_once_with('foo', ANY)
