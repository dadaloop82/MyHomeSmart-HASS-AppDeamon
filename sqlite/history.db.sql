-- SQLite
CREATE TABLE IF NOT EXISTS entity (
	ID integer PRIMARY KEY AUTOINCREMENT,
	HASS_name text NOT NULL,
  friendly_name text NOT NULL,
  attributes text NOT NULL,
  editable integer DEFAULT 0,
	hash text NOT NULL,
  datetime DATETIME DEFAULT CURRENT_TIMESTAMP,
  UNIQUE(hash)
);

CREATE TABLE IF NOT EXISTS state (
	ID integer PRIMARY KEY AUTOINCREMENT,
	state text NOT NULL,
  type text NOT NULL,
  UNIQUE(state)
);

CREATE TABLE IF NOT EXISTS nodes (
	ID integer PRIMARY KEY AUTOINCREMENT,
	prevNodeID integer NOT NULL,
  lastEditableEntityID integer NOT NULL,
  entityID integer NOT NULL,
  stateID integer NOT NULL,
  weight integer NOT NULL,
  datetime DATETIME DEFAULT CURRENT_TIMESTAMP
);