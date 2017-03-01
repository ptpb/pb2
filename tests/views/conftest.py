from unittest.mock import patch

import pytest

from pb.main import init
from pb.storage.base import BaseStorage


@pytest.fixture
@patch.multiple(BaseStorage, __abstractmethods__=set())
def cli(loop, test_client):

    app = init(loop=loop, argv=None)
    app['storage'] = BaseStorage()

    return loop.run_until_complete(test_client(app))
