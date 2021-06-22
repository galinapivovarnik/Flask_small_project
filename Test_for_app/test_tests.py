import pytest


def test_index(client, auth):
    assert client.get('/').status_code == 200

    response = client.get('/')
    assert b'Register' in response.data
    assert b'Log in' in response.data
    assert b'Log out' not in response.data

    auth.login()
    response = client.get('/')
    assert b'Log out' in response.data
    assert b'Show all available tests' in response.data
    assert b'Create test' in response.data


@pytest.mark.parametrize('path', ('/creating_tests', '/all_tests/1',))
def test_login_required(client, path):
    response = client.get(path)
    assert response.headers['Location'] == 'http://localhost/login'


def test_create_tests(client, auth):
    auth.login()
    assert client.get('/creating_tests').status_code == 200


@pytest.mark.parametrize(('test_title', 'test_q_count', 'test_a_count', 'message'),
                         (('', '1', '2', b'Title is required.'),
                         ('1', '', '2', b'Count of questions is required.'),
                         ('1', '1', '', b'Count of answers is required.'),
                         ('1', '1', '2', None)))
def test_create_tests_validate_input(client, auth, test_title, test_q_count, test_a_count, message):
    auth.login()
    response = client.post('/creating_tests', data={'test_title': test_title, 'test_q_count': test_q_count,
                                                    'test_a_count': test_a_count})

    if message is not None:
        assert message in response.data
    else:
        assert 'http://localhost/creating_tests/q_a' in response.headers['Location']
        assert client.get('/creating_tests/q_a').status_code == 200


def test_all_tests(client, auth):
    auth.login()
    assert client.get('/all_tests').status_code == 200

    response = client.get('/all_tests')
    assert b'Delete' in response.data
