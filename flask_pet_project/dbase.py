import sqlite3
from flask import current_app
from flask import g
from flask.cli import with_appcontext

import click


def get_db():
    """Function for getting connection with our sqlite3-database"""

    if 'db' not in g:
        g.db = sqlite3.connect(current_app.config['DATABASE'])
        g.db.row_factory = sqlite3.Row
    return g.db


def close_db(e=None):
    """Function to close db-connection, if any."""

    db = g.pop('db', None)
    if db is not None:
        db.close()


def init_db():
    """Function for executing sql-file for creating tables."""

    # Clear existing data and create new tables.
    db = get_db()

    with current_app.open_resource("schema.sql") as f:
        db.executescript(f.read().decode("utf8"))
    print('init_db')


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Function for initialising new command 'init-db' for our flask-application."""

    # Clear existing data and create new tables.
    print(f'{current_app}')
    init_db()
    click.echo("Initialized the database.")


def init_app(app):
    """This function register database functions with the Flask app.
    This is called by the application factory."""

    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)  # allows use command in terminal
