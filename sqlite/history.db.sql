-- SQLite
CREATE TABLE IF NOT EXISTS entity (
	ID integer PRIMARY KEY AUTOINCREMENT,
	HASS_name text NOT NULL,
  friendly_name text NOT NULL,
  attributes text NOT NULL,
  editable integer DEFAULT 0,
	check_md5 text NOT NULL,
  UNIQUE(HASS_name)
);

CREATE TABLE IF NOT EXISTS state (
	ID integer PRIMARY KEY AUTOINCREMENT,
	state text NOT NULL,
  type text NOT NULL  
);

CREATE TABLE IF NOT EXISTS nodes (
	ID integer PRIMARY KEY AUTOINCREMENT,
	prevNodeID integer NOT NULL,
  entityID integer NOT NULL,
  stateID integer NOT NULL,
  weight integer NOT NULL,
  datetime DATETIME DEFAULT CURRENT_TIMESTAMP
);