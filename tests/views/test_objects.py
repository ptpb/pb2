from unittest.mock import ANY

from aiohttp import multipart
from asynctest import patch

from pb.storage.base import BaseStorage


@patch.object(BaseStorage, 'create_object', return_value={})
async def test_object_post(mock_create_object, cli):
    with multipart.MultipartWriter() as writer:
        writer.append('test')

    await cli.post('/objects', data=writer, headers=writer.headers)

    assert mock_create_object.call_count == 1


@patch.object(BaseStorage, 'read_object')
async def test_object_get(mock_read_object, cli):
    await cli.get('/object/foo')

    assert mock_read_object.call_count == 1
    mock_read_object.assert_called_once_with('foo', ANY)
