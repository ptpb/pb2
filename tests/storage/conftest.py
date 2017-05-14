import pytest

from pb.utils.hash import hash_function


@pytest.fixture
def digest():
    return hash_function()
