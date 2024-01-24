ALTER TABLE sources ADD creation_date2 TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP;
UPDATE sources SET creation_date2 = creation_date2 WHERE creation_date IS NOT NULL;
ALTER TABLE sources DROP creation_date;
ALTER TABLE sources RENAME COLUMN creation_date2 TO creation_date;

PRAGMA user_version=6;