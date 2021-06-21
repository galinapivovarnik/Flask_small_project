import pytest
from flask_pet_project.dbase import get_db


def test_index(client, auth):
    response = client.data('/')
    assert b'Register' in response.data
    assert b'Log in' in response.data
    assert b'Log out' not in response.data

    auth.login()
    response = client.data('/')
    assert b'Log out' in response.data
    assert b'Show all available tests' in response.data
    assert b'Create test' in response.data

@pytest.mark.parametrize('path', ('/creating_tests', '/all_tests/<test_id>',))
def test_login_required(client, path):

