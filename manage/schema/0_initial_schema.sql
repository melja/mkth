BEGIN TRANSACTION;

DROP TABLE IF EXISTS author_names;
DROP TABLE IF EXISTS authors;
DROP TABLE IF EXISTS user_names;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS name_parts;
DROP TABLE IF EXISTS name_format_part_types;
DROP TABLE IF EXISTS name_part_types;
DROP TABLE IF EXISTS names;
DROP TABLE IF EXISTS name_formats;
DROP TABLE IF EXISTS timezones;
DROP TABLE IF EXISTS reference_data_sources;

CREATE TABLE IF NOT EXISTS reference_data_sources (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    external_id TEXT NOT NULL,
    version TEXT NOT NULL,
    title TEXT NULL,
    url TEXT NULL,
    steward TEXT NULL,
    license TEXT NULL,
    retrieved TEXT NOT NULL,
    UNIQUE (external_id, version)
);

CREATE TABLE IF NOT EXISTS timezones (
    region TEXT NOT NULL,
    timezone TEXT NOT NULL,
    metazone TEXT NULL,
    reference_data_source_id INT NOT NULL,
    PRIMARY KEY (region, timezone),
    FOREIGN KEY (reference_data_source_id) REFERENCES reference_data_sources ( id )
);

CREATE TABLE IF NOT EXISTS name_formats (
    name_format TEXT NOT NULL PRIMARY KEY,
    description TEXT NOT NULL UNIQUE,
    reference_data_source_id INT NOT NULL,
    FOREIGN KEY (reference_data_source_id) REFERENCES reference_data_sources ( id )
);

CREATE TABLE IF NOT EXISTS name_part_types (
    name_part_type TEXT NOT NULL PRIMARY KEY,
    description TEXT NOT NULL,
    reference_data_source_id INT NOT NULL,
    FOREIGN KEY (reference_data_source_id) REFERENCES reference_data_sources ( id )
);

CREATE TABLE IF NOT EXISTS name_format_part_types (
    name_format TEXT NOT NULL,
    name_part_type TEXT NOT NULL,
    part_ordinal INTEGER NOT NULL,
    reference_data_source_id INT NOT NULL,
    UNIQUE (name_format, part_ordinal),
    PRIMARY KEY (name_format, name_part_type),
    FOREIGN KEY (name_format) REFERENCES name_formats (name_format)
    FOREIGN KEY (name_part_type) REFERENCES name_part_types (name_part_type),
    FOREIGN KEY (reference_data_source_id) REFERENCES reference_data_sources ( id )
);

CREATE TABLE IF NOT EXISTS names (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    name_format TEXT NOT NULL,
    creation_date TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_updated TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (name_format) REFERENCES name_formats (name_format)
);

CREATE TABLE IF NOT EXISTS name_parts (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    name_id INTEGER NOT NULL,
    name_part_type TEXT NOT NULL,
    name_part TEXT NOT NULL,
    part_ordinal INT NOT NULL,
    UNIQUE (name_id, part_ordinal),
    FOREIGN KEY (name_id) REFERENCES names (id),
    FOREIGN KEY (name_part_type) REFERENCES name_part_types (name_part_type)
);

CREATE TABLE IF NOT EXISTS users (
  id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  creation_date TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
  access_enabled CHAR(1) NOT NULL DEFAULT 'Y',
  password TEXT NULL,
  password_last_updated TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
  display_name TEXT UNIQUE NULL,
  preferred_name TEXT NULL,
  email TEXT NULL,
  timezone TEXT NULL,
  display_language TEXT NULL 
);

CREATE TABLE IF NOT EXISTS user_names (
    user_id INTEGER NOT NULL,
    name_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users (id),
    FOREIGN KEY (name_id) REFERENCES names (id),
    PRIMARY KEY (user_id, name_id)
);

CREATE TABLE IF NOT EXISTS authors (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    display_name TEXT NOT NULL,
    creation_date TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_updated TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS author_names (
    author_id INTEGER NOT NULL,
    name_id INTEGER NOT NULL,
    FOREIGN KEY (author_id) REFERENCES authors (id),
    FOREIGN KEY (name_id) REFERENCES names (id),
    PRIMARY KEY (author_id, name_id)
);

PRAGMA user_version=0;

COMMIT TRANSACTION;