import pytest
from flask_pet_project.dbase import get_db
from flask import session, request


def test_index(client, auth):
    assert client.get('/').status_code == 200

    response = client.data('/')
    assert b'Register' in response.data
    assert b'Log in' in response.data
    assert b'Log out' not in response.data

    auth.login()
    response = client.data('/')
    assert b'Log out' in response.data
    assert b'Show all available tests' in response.data
    assert b'Create test' in response.data


@pytest.mark.parametrize('path', ('/creating_tests', '/all_tests/1',))
def test_login_required(client, path, auth):
    auth.login()
    response = client.post(path)
    assert response.headers['Location'] == f'http://localhost/{path}'

    auth.logout()
    assert response.headers['Location'] == 'http://localhost/login'


def test_create_tests(client, auth):
    auth.login()
    assert client.get('/create_tests').status_code == 200
    response = client.get('/create_tests')
    assert session['test_id'] is None


@pytest.mark.parametrize(('test_title', 'test_q_count', 'test_a_count', 'message'), (('', '1', '1', b'Title is required.'),
                         ('1', '', '1', b'Count of questions is required.'),
                         ('1', '1', '', b'Count of answers is required.')))
def create_tests_validate_input(client, auth, test_title, test_q_count, test_a_count, message):
    auth.login()
    response = client.post('/create_tests', data={'test_title': test_title, 'test_q_count': test_q_count,
                                                  'test_a_count': test_a_count, 'message': message})
    assert message in response.data
    assert 'http://localhost/creating_tests/q_a' in response.headers['Location']


def test_create_tests_2(client, auth):
    auth.login()
    assert client.get('/create_tests_2').status_code == 200


def create_tests_2_validate_input(client, auth, q=2, a=2):
    auth.login()
    response = client.post('/create_tests_2')
    for i in q:
        if not request.form[f'question{i+1}']:
            assert f'You didn\'t specify question {i+1}.' in response.text

    for i in a:
        if not request.form[f'answer{i+1}']:
            assert f'You didn\'t fill some answer field.' in response.text

    assert 'http://localhost/all_tests' in response.headers['Location']


@pytest.mark.parametrize('path2', ('all_tests/1', 'all_tests/2', 'all_tests/3', 'all_tests/4', 'all_tests/5',
                                   'all_tests/6', 'all_tests/7', 'all_tests/8'))
def test_all_tests(client, auth, path2):
    auth.login()
    assert client.get('/all_tests').status_code == 200
    response = client.post('/all_tests')
    assert f'http://localhost/{path2}' in response.headers['Location']


@pytest.mark.parametrize('test_id', ('1', '2', '3', '4', '5', '6', '7', '8'))
def test_test_var(client, auth, test_id):
    auth.login()
    assert client.get(f'all_tests/{test_id}').status_code == 200

    response = client.post(f'all_tests/{test_id}')
    assert f'http://localhost/results/{test_id}' in response.headers['Location']


@pytest.mark.parametrize('test_id', ('1', '2', '3', '4', '5', '6', '7', '8'))
def test_test_results(client, test_id):
    assert client.get(f'results/{test_id}').status_code == 200

    response = client.get(f'results/{test_id}')
    assert b'<< Try again' in response.data
    assert b'Return to main page >>' in response.data


