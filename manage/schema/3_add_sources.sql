CREATE TABLE sources (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  title TEXT UNIQUE NULL NULL,
  authorid INTEGER NOT NULL, 
  creation_date TEXT NOT NULL,
  CONSTRAINT FK_sources_authorid FOREIGN KEY (authorid) REFERENCES authors (id)
);

PRAGMA user_version = 3;