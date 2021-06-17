import sqlite3

import pytest
from flask_pet_project.dbase import get_db


def test_get_close_dbase(app):
    with app.app_contest():
        # Checking if the data bases return the same connection each time
        db = get_db()
        assert db is get_db()

    # Call correspond error during sql-request
    with pytest.raises(sqlite3.ProgrammingError) as e:
        db.execute('SELECT 1')
    # Get access to the information about raised error
    assert 'closed' in str(e.value)


# Це я поки майже не розумію як працює і для чого:
def test_init_db_command(runner, monkeypatch):
    class Recorder:
        called = False

    def fake_init_db():
        Recorder.called = True

    # For dynamic modification of 'init_db', set attribute 'fake_init_db'
    monkeypatch.setattr('flask_pet_project.dbase.init_db', fake_init_db)
    result = runner.invoke(args=['init-db'])  # Launching 'init-db' command

    assert 'Initialized' in result.output
    assert Recorder.called
