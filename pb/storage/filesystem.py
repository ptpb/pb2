from os import path

import aiofiles
from xdg import BaseDirectory

from pb.models.paste import Paste
from pb.utils.datetime import now
from pb.utils.hash import hash_function
from pb.utils.json import JSONEncoder


base_directory = BaseDirectory.save_data_path('pb', 'paste')


async def _write_body(filename, body_part, digest):
    size = 0
    async with aiofiles.open(filename, mode='wb') as f:
        while True:
            chunk = await body_part.read_chunk()
            if not chunk:
                break

            size += len(chunk)
            digest.update(chunk)

            await f.write(chunk)

    return size


async def write_body(body_part):

    paste = Paste.create()
    digest = hash_function()

    filename = path.join(base_directory, str(paste.uuid))
    size = await _write_body(filename, body_part, digest)

    paste.digest = digest.digest()
    paste.size = size
    paste.create_dt = now()

    return paste


async def _write_metadata(filename, metadata):
    async with aiofiles.open(filename, mode='w') as f:
        await f.write(metadata)


async def write_metadata(paste):
    filename = path.join(base_directory, '{}_metadata'.format(paste.uuid))
    metadata = JSONEncoder().encode(paste.asdict())

    await _write_metadata(filename, metadata)


# fixme: stub
async def stub(name, stream):
    filename = path.join(base_directory, name)

    async with aiofiles.open(filename, mode='rb') as f:
        while True:
            chunk = await f.read(8192)
            if not chunk:
                break

            stream.write(chunk)
