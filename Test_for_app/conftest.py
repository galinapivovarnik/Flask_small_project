import os
import tempfile

import pytest
from flask_pet_project import create_app
from flask_pet_project.dbase import get_db, init_db

# Open file with test data:
with open('.test_data.sql') as f:
    test_data_sql_ = f.read()


@pytest.fixture
def app():
    # Create and open temporary file (db_f - file object; db_path - the path to file object)
    db_f, db_path = tempfile.mkstemp()

    app = create_app({
        'TESTING': True,
        'DATABASE': db_path,
    })

    # Initialization of DB and execute our test data
    with app.app_context():
        init_db()
        get_db().executescript(test_data_sql_)

    yield app

    # Closing temporary file and delete the path to it:
    os.close(db_f)
    os.unlink(db_path)


# For making request to the application without running the server:
@pytest.fixture
def client(app):
    return app.test_client()


# For creating a runner that can call Click commands (which are registered with the application):
@pytest.fixture
def runner(app):
    return app.test_cli_runner()


# For most of the view user should be logged in, so we create class for that:
class AuthAction:
    def __init__(self, client):
        self._client = client

    def login(self, username='test', password='test'):
        # return expected results from 'POST'-method
        return self._client.post('/login', data={'username': username, 'password': password})

    def logout(self):
        return self._client.get('/logout')


@pytest.fixture
def auth(client):
    return AuthAction(client)
