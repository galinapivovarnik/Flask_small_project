from werkzeug.security import generate_password_hash, check_password_hash
from flask import Blueprint, render_template, url_for, request, flash, redirect, session
from . import dbase

bp = Blueprint('auth', __name__)


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = dbase.get_db()

        # Set up the error variable for flash message:
        error = None
        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif db.cursor().execute('SELECT id from user WHERE username=?', (username,)).fetchone() is not None:
            error = f'User with name "{username}" is already exist.'

        # Saving data to the DB:
        if error is None:
            db.cursor().execute('INSERT INTO user(username, password) VALUES (?, ?)',
                                (username, generate_password_hash(password)))
            db.commit()
            session['user_id'] = None
            return redirect(
                url_for('.login'))  # ??? ще не можу перевірити чи це працює, бо там помилки з бд перед цим раніше
        flash(error)
    session['user_id'] = None
    return render_template('register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = dbase.get_db().cursor()

        # Set up the error variable for flash message:
        error = None
        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        user = db.execute('SELECT * FROM user WHERE username = ?', (username,)).fetchone()
        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        # Saving data for the session:
        if error is None:
            session.clear()
            session['user_id'] = user['id']
            session['user_name'] = user['username']
            return redirect(url_for('index'))

        flash(error)

    session['user_id'] = None
    session['user_name'] = None

    return render_template('login.html')


@bp.route('/logout')
def logout():
    session['user_id'] = None
    session.clear()
    return redirect(url_for('index'))
