from os import walk, path, getcwd
import sqlite3
import click
import json
from flask import current_app, g
from datetime import datetime

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

def upsert_row_data_from_json(json_data):
    db = get_db()
    db_version = get_user_version(db)
    if "schema_version" not in json_data:
        raise(ValueError("Import file does not contain a 'schema_version' key"))
    import_schema_version = json_data["schema_version"]
    if import_schema_version != db_version:
        raise(ValueError(f"Database schema version {db_version} and import schema version {import_schema_version} do not match"))
    if "data_format" not in json_data:
        raise(ValueError("Import file does not contain a 'data_format' key"))
    data_format = json_data["data_format"]
    if data_format != 0:
        raise(ValueError(f"Import file data format {data_format} does not match expected data format of 0"))
    if "table_data" not in json_data:
        raise(ValueError("Import file does not contain the expected 'table_data' key"))
    if "datasource" not in json_data:
        raise(ValueError("Import file does not contain the expected 'datasource' key"))
    datasource = json_data["datasource"]
    datasource_id = None
    if "id" in datasource:
        datasource_id = datasource["id"]
    version = None
    if "version" in datasource:
        version = datasource["version"]
    title = None
    if "title" in datasource:
        title = datasource["title"]
    retrieved = datetime.utcnow().isoformat()
    if "retrieved" in datasource:
        retrieved = datasource["retrieved"]
    steward = None
    if "steward" in datasource:
        steward = datasource["steward"]
    license = None
    if "license" in datasource:
        license = datasource["license"]
    url = None
    if "url" in datasource:
        url = datasource["url"]
    if datasource_id and version:
        db.execute("INSERT INTO reference_data_sources (external_id, version, title, retrieved, steward, license, url)"
                    " VALUES ( ?, ?, ?, ?, ?, ?, ?) "
                    " ON CONFLICT ( external_id, version ) DO UPDATE SET title=excluded.title, retrieved=excluded.title, steward=excluded.steward, license=excluded.license, url=excluded.url; ",
                    (datasource_id, version, title, retrieved, steward, license, url,))
    ref_data_source = db.execute("SELECT id FROM reference_data_sources WHERE external_id = ? and version = ?;", (datasource_id, version)).fetchone()
    ref_data_source_id = ref_data_source["id"]
    for table_data in json_data["table_data"]:
        tablename = table_data["tablename"]
        columns = table_data["columns"]
        columns.append("reference_data_source_id")
        key_columns = table_data["key_columns"]
        tokens = ', '.join(["?"] * len(columns))
        updates = ', '.join(list((f"{col}=excluded.{col}" for col in columns if col not in key_columns)))
        upsert = f"INSERT INTO {tablename} ( {', '.join(columns)} ) VALUES ( {tokens} ) ON CONFLICT ( {', '.join(key_columns)} ) DO UPDATE SET { updates };"
        row_data = [tuple(row)+(ref_data_source_id,) for row in table_data["row_data"]]
        db.executemany(upsert, row_data)
        db.commit()

def init_db():
    db = get_db()
    with current_app.open_resource(f"schema/0_initial_schema.sql") as f:
        db.executescript(f.read().decode('utf8'))
        db.commit()

def migrate_db():
    # A trivially simple migration strategy:
    #
    # The schema version is stored in the SQLIte PRAGMA user_version
    # List *.sql files in the schema dir with a higher version number than in the database
    # Apply each one in order to the database and update the user_version PRAGMA
    click.echo("Looking for schema files to apply to the database.")
    db = get_db()

    db_ver = get_user_version(db)
    files = []
    for (dirpath, dirnames, filenames) in walk("manage/schema"):
        files.extend(filenames)
    
    allschema = [f for f in files if path.splitext(f)[1].lower() == ".sql"]
    toapply = sorted([f for f in allschema if int(f.split("_")[0]) > db_ver])
    for file in toapply:
        with current_app.open_resource(f"schema/{file}") as f:
            print(f"Applying schema file {file}")
            db.executescript(f.read().decode('utf8'))
    db.commit()
    new_ver = get_user_version(db)
    click.echo(f"Done updating schema. Existing version {db_ver}, current version {new_ver}.")

def load_reference_data():
    click.echo("Loading reference data into the database.")
    try:
        files = []
        for (dirpath, dirnames, filenames) in walk("manage/reference_data"):
            files.extend(filenames)
        
        data_files = [f for f in files if path.splitext(f)[1].lower() == ".json"]
        for file in data_files:
            with current_app.open_resource(f"reference_data/{file}") as f:
                print(f"Loading data from {file}")
                str_data = f.read()
                json_data = json.loads(str_data)
                upsert_row_data_from_json(json_data)
        click.echo("Successfully loaded data")
    except ValueError as e:
        print(f"IMPORT ERROR: {e}") 

def load_test_users():
    db = get_db()
    users = [("melja",
               "melja@pobox.com",
               "scrypt:32768:8:1$GHtkCim9P3USWnud$da12c3c1c701ef7c7775041cd4f9585287a930bf0e810d1d741ff60b035689ad3799a33a437f4e18cc0f3b6610905f772b6cf88c1c87ebdc95983e17dcf18ea1",
               "John Melendy",
               "US/Pacific",
               "US/en",),
               ("test",
               "test@meljh.com",
               "scrypt:32768:8:1$GHtkCim9P3USWnud$da12c3c1c701ef7c7775041cd4f9585287a930bf0e810d1d741ff60b035689ad3799a33a437f4e18cc0f3b6610905f772b6cf88c1c87ebdc95983e17dcf18ea1",
               "Test User",
               "Europe/London",
               "GB/en",)]
    db.executemany("INSERT INTO users (username, email, password, display_name, timezone, display_language) "
               " VALUES ( ?, ?, ?, ?, ?, ?) "
               " ON CONFLICT(username) DO NOTHING "
               " ON CONFLICT(display_name) DO NOTHING;",
               users
    )
    db.commit()

@click.command('init-db')
def init_db_command():
    click.echo("Dropping and recreating all schema.")
    init_db()
    migrate_db()
    load_reference_data()
    click.echo("Done initializing the database.")

@click.command('migrate-db')
def migrate_db_command():
    migrate_db()

@click.command('load-ref-data')
def load_ref_data_command():
    load_reference_data()

@click.command('load-test-data')
def load_test_data_command():
    click.echo("Loading test data into the database.")
    from . import test_data
    test_data.load_test_data(get_db())

@click.command('load-test-users')
def load_test_users_command():
    click.echo("Loading test users")
    load_test_users()


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
    app.cli.add_command(load_ref_data_command)
    app.cli.add_command(migrate_db_command)
    app.cli.add_command(load_test_data_command)
    app.cli.add_command(load_test_users_command)
