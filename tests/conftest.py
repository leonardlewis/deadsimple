import pytest

class DB(object):
    pass

@pytest.fixture(scope="session")
def db():
    return DB()
