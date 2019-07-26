import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext

from app import app

import config

app.config.from_object('config')

def init_app(app):
    app.teardown_appcontext(close_connection)
    app.cli.add_command(init_db_command)

def get_db():
    # db = getattr(g, '_database', None)
    # if db is None:
    #     db = g._database = sqlite3.connect(app.config['DATABASE'])
    # #db.row_factory = sqlite3.Row
    #
    if 'db' not in g:
        g.db = sqlite3.connect(
            app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
        #db.row_factory = make_dicts
    return g.db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def make_dicts(cursor, row):
    return dict((cursor.description[idx][0], value)
                for idx, value in enumerate(row))

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = [dict((cur.description[idx][0], value)
               for idx, value in enumerate(row)) for row in cur.fetchall()]
    return (rv[0] if rv else None) if one else rv


def init_db():
    with app.app_context():
        db = get_db()
        with open(app.config['INIT_SCHEMA'], mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

@click.command('init-db')
@with_appcontext
def init_db_command():

    """Clear the existing data and create new tables."""
    click.echo("Initializing by " + app.config['INIT_SCHEMA'])

    init_db()
    click.echo('Initialized the database.')
