# os library
import os
# sqlite3 library
import sqlite3
# Constants
import module.constant as CONSTANT
# Logging functions
import module.log as LOG

# Global Class variable
DBConn = {}                     # DB Connections


def create(self: any, dbName: str) -> bool:
    """create Sqlite3 db from sql queries

    Args:
        self (any):         The appDeamon HASS Api
        dbName (str):       database Name

    Returns:
        bool:               True/False (False means errors)
    """
    try:
        if not os.path.exists(CONSTANT.DBPath):
            os.makedirs(CONSTANT.DBPath)
        _dbConn = sqlite3.connect(
            dbName, check_same_thread=False)
        sql_file = open(os.path.join(
            CONSTANT.NEWDB_Sql_path, os.path.basename(dbName)) + ".sql")
        sql_as_string = sql_file.read()
        _cur = _dbConn.cursor()
        _cur.executescript(sql_as_string)
        LOG.info(self, "DB created: %s" % (dbName))
        _dbConn.close()
        return True
    except Exception as e:
        """ There has been an error """
        LOG.info(self, "DB creation: %s" % (dbName))
        LOG.error(self, e, True)
        return False


def connect(self: any, dbPath: str, dbName: str) -> bool:
    """connect to Sqlite3 db and store the connection object in global variable

    Args:
        self (any):         The appDeamon HASS Api
        dbPath (str):       database Path
        dbName (str):       database Name

    Returns:
        bool: _description_
    """
    if not dbName in DBConn:
        try:
            DBConn[dbName] = sqlite3.connect(
                dbPath, check_same_thread=False)
            LOG.info(self, "DB ready: %s" % (dbName))
            return True
        except Exception as e:
            """ There has been an error """
            LOG.info(self, "DB connect: %s" % (dbName))
            LOG.error(self, e, True)
            return False
    return True


def query(self: any, query: str, dbName: str, fetchOne: bool = False, **kwargs) -> dict:
    """make a query to dbName (any query are allowed)

    Args:
        self (any):                 The appDeamon HASS Api
        query (str):                The query
        dbName (str):               The database name
        fetchOne (bool, optional):  Fetch only one element/all elements Defaults to False.
    Raises:
        ValueError: _description_

    Returns:
        dict: _description_
    """
    try:
        if not dbName in DBConn:
            LOG.error(self, "DB %s is not ready" % (dbName), True)
        _cur = DBConn[dbName].cursor()
        if kwargs:
            query = query.format(**kwargs)
        if CONSTANT.DEBUG_DB:
            self.log("[ %s ]" % (query))
        _cur.execute(query)
        if "SELECT" in query:
            if fetchOne:
                return _cur.fetchone()
            else:
                return _cur.fetchall()
        else:
            DBConn[dbName].commit()
            if "selectQuery" in kwargs:
                _cur.execute(kwargs["selectQuery"])
                return _cur.fetchone()[0]
            return _cur.lastrowid
    except sqlite3.Error as e:
        """ There has been an error """
        LOG.error(self, e, True)
        return False
