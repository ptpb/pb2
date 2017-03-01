import asyncio
from io import BytesIO

import pytest


def read_chunk(body):
    return asyncio.coroutine(BytesIO(body).read)


@pytest.mark.asyncio
async def test_create_object(fs, storage, digest):
    body = b'test1234'
    digest.update(body)

    obj = await storage.create_object(read_chunk(body))

    assert obj.digest == digest.digest()

    assert fs.Exists(storage.object_path(obj.uuid, 'body'))
    assert fs.Exists(storage.object_path(obj.uuid, 'metadata'))


@pytest.mark.asyncio
async def test_read_object(fs, storage, digest):
    body = b'test1234'
    digest.update(body)
    bio = BytesIO()

    obj1 = await storage.create_object(read_chunk(body))
    obj2 = await storage.read_object(obj1.uuid, bio.write)

    assert obj1 == obj2
    assert bio.getvalue() == body
