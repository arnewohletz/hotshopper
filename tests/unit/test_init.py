"""
Test hotshopper.__init__.py
"""

# Intra-package imports
import hotshopper


class TestDatabaseInitialization:
    def test_init_database_from_file(self, no_test_mode):
        db = hotshopper.get_db()

        assert db is not None
        assert "sqlite:///:memory:" not in str(db.engine.url)

    def test_init_test_database(self, test_mode):
        db = hotshopper.get_db()

        assert db is not None
        assert "sqlite:///:memory:" in str(db.engine.url)
