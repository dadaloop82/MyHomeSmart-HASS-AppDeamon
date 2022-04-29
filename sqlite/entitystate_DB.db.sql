-- SQLite
CREATE TABLE IF NOT EXISTS entity (
	ID integer PRIMARY KEY AUTOINCREMENT,
	HASS_name text NOT NULL,
  friendly_name text NOT NULL,
  attributes text NOT NULL,
  editable integer DEFAULT 0,	
  datetime DATETIME DEFAULT CURRENT_TIMESTAMP,
  UNIQUE(HASS_name)
);

CREATE TABLE IF NOT EXISTS state (
	ID integer PRIMARY KEY AUTOINCREMENT,
	value text NOT NULL,
  type text NOT NULL,  
  numvalue_min integer DEFAULT 0,
  numvalue_max integer DEFAULT 0,
  frequency integer DEFAULT 0
);

CREATE TABLE IF NOT EXISTS entitystate (
	ID integer PRIMARY KEY AUTOINCREMENT,	  
  entityID integer NOT NULL,
  stateID integer NOT NULL,
  count integer NOT NULL,
  datetime DATETIME DEFAULT CURRENT_TIMESTAMP
);