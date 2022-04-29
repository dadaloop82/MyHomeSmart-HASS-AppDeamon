-- SQLite
CREATE TABLE IF NOT EXISTS nodeslink (
	ID integer PRIMARY KEY AUTOINCREMENT,
	cause_entityID integer NOT NULL,
  operator text NOT NULL,
  affected_entityID integer NOT NULL,
  type text NOT NULL,
	min_max text NOT NULL
);