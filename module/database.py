# os library
import os
# sqlite3 library
import sqlite3
# Constants
import module.constant as CONSTANT
# Logging functions
import module.log as LOG

DBConn = {}


def create(self: any, dbName: str) -> bool:
    """create Sqlite3 db from sql queries

    Args:
        self (any):         The appDeamon HASS Api
        dbName (str):       database Name

    Returns:
        bool:               True/False (False means errors)
    """
    try:
        _dbConn = sqlite3.connect(
            dbName, check_same_thread=False)
        sql_file = open(os.path.join(
            CONSTANT.NEWDB_Sql_path, os.path.basename(dbName)) + ".sql")
        sql_as_string = sql_file.read()
        _cur = _dbConn.cursor()
        _cur.executescript(sql_as_string)
        self.log("DB created: %s" % (dbName))
        _dbConn.close()
        return True
    except Exception as e:
        """ There has been an error """
        LOG.LogError(self, e, True)
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
            self.log("DB ready: %s" % (dbName))
            return True
        except Exception as e:
            """ There has been an error """
            LOG.LogError(self, e, True)
            return False
    return True
