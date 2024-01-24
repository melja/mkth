ALTER TABLE authors ADD creation_date2 TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP;
UPDATE authors SET creation_date2 = creation_date2 WHERE creation_date IS NOT NULL;
ALTER TABLE authors DROP creation_date;
ALTER TABLE authors RENAME COLUMN creation_date2 TO creation_date;

PRAGMA user_version=5;