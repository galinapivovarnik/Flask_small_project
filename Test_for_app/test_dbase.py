import sqlite3

import pytest
from ..flask_pet_project.dbase import get_db, init_db


def test_get_close_dbase(app):
    with app.app_context():
        # Checking if the data bases return the same connection each time
        db = get_db()
        assert db is get_db()

    # Call correspond error during sql-request (u can't connect to db because it was closed earlier)
    with pytest.raises(sqlite3.ProgrammingError) as e:
        db.execute('SELECT 1')
    # Get access to the information about raised error
    assert 'closed' in str(e.value)

