import os

import pytest

from hotshopper import get_db, create_application


@pytest.fixture(scope='function')
def no_test_mode():
    os.environ["TEST_MODE"] = "False"
    create_application()


@pytest.fixture(scope='function')
def test_mode():
    os.environ["TEST_MODE"] = "True"
    create_application()


@pytest.fixture(scope="function")
def test_db():
    os.environ["TEST_MODE"] = "True"
    create_application()
    test_db = get_db()
    yield test_db
    test_db.session.remove()
    test_db.drop_all()
