"""
Test hotshopper.__init__.py
"""

# Standard Library imports
from importlib import reload
import os
from unittest import mock

# PyPI third-party imports
import pytest

from hotshopper import get_db


@pytest.fixture(scope='function')
def no_test_mode():
    os.environ["TEST_MODE"] = "False"
    yield
    os.environ["TEST_MODE"] = "True"

# @pytest.fixture(scope='function')
# def test_mode():
#     os.environ["TEST_MODE"] = "True"
#     yield
#


class TestDatabaseInitialization:
    @mock.patch.dict(os.environ, {"TEST_MODE": "False"})
    def test_init_database_from_file(self):
        db = get_db()
        # del get_db
        # breakpoint()
        assert not db is None
        assert not "sqlite:///:memory" in db.engine.url

    @mock.patch.dict(os.environ, {"TEST_MODE": "True"})
    def test_init_test_database(self):
        # reload(get_db())
        # breakpoint()
        db = get_db()
        # del get_db
        assert not db is None
        # breakpoint()
        assert "sqlite:///:memory:" is db.engine.url
