# os library
import os
# sqlite3 library
import sqlite3
# Constants
import module.constant as CONSTANT
# Logging functions
import module.log as LOG


def createDB(self: any, dbName: str):
    try:
        _dbConn = sqlite3.connect(
            dbName, check_same_thread=False)
        sql_file = open(os.path.join(
            CONSTANT.NEWDB_Sql_path, os.path.basename(dbName)) + ".sql")
        sql_as_string = sql_file.read()
        _cur = _dbConn.cursor()
        _cur.executescript(sql_as_string)
        return True
    except Exception as e:
        """ There has been an error """
        LOG.LogError(self, e, True)
        return False
