import pytest
from flask import g, session, Response
from flask_pet_project.dbase import get_db


def test_register(client, app):
    # client.get - makes a get-request and return the Response object
    assert client.get('/register').status_code == 200

    # client.post - makes a post-request and converting the data-dict into form data
    # data - contains the body of the response as bytes
    response = client.post('/register', data={'username': 'a', 'password': 'a'})
    # response.text - вертає текст сторінки (напр html-файл або те що вертає ф-ція...)
    assert 'http://localhost/login' == response.headers['Location']

    with app.app_context():
        assert get_db().execute('SELECT * FROM user WHERE username = "a" ').fetchone() is not None


# @pytest.mark.parametrize - tells Pytest to run the same function with different arguments
@pytest.mark.parametrize(('username', 'password', 'message'),
                         (('', '', b'Username is required.'), ('a', '', b'Password is required.'),
                          ('test', 'test', b'User with name test is already exist.')))
def register_validate_input(client, username, password, message):
    response = client.post('/register', data={'username': username, 'password': password})
    assert message in response.data


def test_login(client, app, auth):
    # client.get - makes a get-request and return the Response object
    assert client.get('/login').status_code == 200
    response = auth.login() 
    assert 'http://localhost/' == response.headers['Location']

    with client:
        client.get('/')
        assert session['username'] == 'test'


# @pytest.mark.parametrize - tells Pytest to run the same function with different arguments
@pytest.mark.parametrize(('username', 'password', 'message'),
                         (('a', 'test', b'Incorrect username.'), ('test', 'a', b'Incorrect password.'), ))
def login_validate_input(auth, username, password, message):
    response = auth.login(username, password)
    assert message in response.data  # response.data - як response.text , але у байтах


def test_logout(client, auth):
    auth.login()

    with client:
        auth.logout()
        assert 'user_id' not in session
