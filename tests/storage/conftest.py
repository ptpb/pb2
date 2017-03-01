from aiofiles import threadpool
from aiofiles.threadpool.binary import AsyncBufferedIOBase
from pyfakefs.fake_filesystem import FakeFileWrapper
from pyfakefs.fake_filesystem_unittest import Patcher
import pytest

from pb.storage.filesystem import FilesystemStorage
from pb.utils.hash import hash_function


@pytest.fixture
def fs(request):
    """ Fake filesystem. """
    patcher = Patcher()
    patcher.setUp()

    patcher._stubs.SmartSet(threadpool, '_sync_open', patcher.fake_open)

    request.addfinalizer(patcher.tearDown)
    return patcher.fs


@threadpool.wrap.register(FakeFileWrapper)
def _(file, *, loop=None, executor=None):
    return AsyncBufferedIOBase(file, loop=loop, executor=executor)


@pytest.fixture
def storage():
    storage = FilesystemStorage()
    return storage


@pytest.fixture
def digest():
    return hash_function()
