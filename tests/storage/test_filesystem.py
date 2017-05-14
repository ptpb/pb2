import asyncio
from io import BytesIO

import pytest

from pb.storage.filesystem import FilesystemStorage


@pytest.fixture
def storage():
    storage = FilesystemStorage()
    return storage


def read_chunk(body):
    return asyncio.coroutine(BytesIO(body).read)


@pytest.mark.asyncio
async def test_create_object(afs, storage, digest):
    body = b'test1234'
    digest.update(body)

    obj = await storage.create_object(read_chunk(body))

    assert obj.digest == digest.digest()

    assert afs.Exists(storage.object_path(obj.id, 'body'))
    assert afs.Exists(storage.object_path(obj.id, 'metadata'))


@pytest.mark.asyncio
async def test_read_object(afs, storage, digest):
    body = b'test1234'
    digest.update(body)
    bio = BytesIO()

    obj1 = await storage.create_object(read_chunk(body))
    obj2 = await storage.read_metadata(obj1.id)
    await storage.read_object(obj1.id, bio.write)

    assert obj1 == obj2
    assert bio.getvalue() == body
