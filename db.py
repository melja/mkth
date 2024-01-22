from os import walk, path
import sqlite3
import click
from flask import current_app, g

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def get_user_version(db):
    return db.execute('PRAGMA user_version;').fetchone()["user_version"]


def init_db():
    # A trivially simple migration strategy:
    #
    # The schema version is stored in the SQLIte PRAGMA user_version
    # List *.sql files in the schema dir with a higher version number than in the database
    # Apply each one in order to the database and update the user_version PRAGMA
    db = get_db()

    db_ver = get_user_version(db)
    files = []
    for (dirpath, dirnames, filenames) in walk("schema"):
        files.extend(filenames)
    
    allschema = [f for f in files if path.splitext(f)[1].lower() == ".sql"]
    toapply = sorted([f for f in allschema if int(f.split("_")[0]) > db_ver])
    for file in toapply:
        with current_app.open_resource(f"schema/{file}") as f:
            print(f"Applying schema file {file}")
            db.executescript(f.read().decode('utf8'))


@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)