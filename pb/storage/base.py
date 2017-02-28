from abc import ABCMeta, abstractmethod
from uuid import uuid4

from pb.models.object import Object
from pb.utils.hash import hash_function


class BaseStorage(metaclass=ABCMeta):
    @abstractmethod
    async def _write_body(self, uuid, read_chunk, digest):
        return size  # noqa: F821

    async def write_body(self, uuid, read_chunk):
        digest = hash_function()

        size = await self._write_body(uuid, read_chunk, digest)

        return {
            'uuid': uuid,
            'size': size,
            'digest': digest.digest()
        }

    @abstractmethod
    async def _write_metadata(self, obj_metadata):
        return

    async def write_metadata(self, obj):
        await self._write_metadata(obj.asdict())

    async def create_object(self, read_chunk):
        uuid = uuid4()
        body_metadata = await self.write_body(uuid, read_chunk)

        obj = Object.create(**body_metadata)

        await self.write_metadata(obj)

        return obj

    @abstractmethod
    async def _read_body(self, uuid, write_chunk):
        return

    @abstractmethod
    async def _read_metadata(self, name):
        return obj_metadata  # noqa: F821

    async def read_object(self, name, write_chunk):
        obj_metadata = await self._read_metadata(name)
        obj = Object(**obj_metadata)

        await self._read_body(obj.uuid, write_chunk)

        return obj  # fixme?

    #@abstractmethod
    async def update_object(self):
        return

    #@abstractmethod
    async def delete_object(self):
        return


def setup_storage(app):
    # fixme
    from pb.storage import filesystem

    app['storage'] = filesystem.FilesystemStorage()
