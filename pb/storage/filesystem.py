from os import path

import aiofiles
from xdg import BaseDirectory

from pb.storage.base import StreamStorage
from pb.utils import msgpack


class FilesystemStorage(StreamStorage):
    def __init__(self):
        self.base_directory = BaseDirectory.save_data_path('pb', 'object')

    def object_path(self, id, object_type):
        filename = '{}.{}'.format(str(id), object_type)

        return path.join(self.base_directory, filename)

    async def _write_body(self, id, read_chunk, digest):
        filename = self.object_path(id, 'body')
        size = 0
        async with aiofiles.open(filename, mode='wb') as f:
            while True:
                chunk = await read_chunk()
                if not chunk:
                    break

                size += len(chunk)
                digest.update(chunk)

                await f.write(chunk)

        return size

    async def _write_metadata(self, obj_metadata):
        filename = self.object_path(obj_metadata['id'], 'metadata')
        async with aiofiles.open(filename, mode='wb') as f:
            packed = msgpack.packb(obj_metadata)

            await f.write(packed)

    async def _read_body(self, id, write_chunk):
        filename = self.object_path(id, 'body')
        async with aiofiles.open(filename, mode='rb') as f:
            while True:
                chunk = await f.read(8192)
                if not chunk:
                    break

                write_chunk(chunk)

    async def _read_metadata(self, name):
        filename = self.object_path(name, 'metadata')
        async with aiofiles.open(filename, mode='rb') as f:
            packed = await f.read()

            return msgpack.unpackb(packed)
