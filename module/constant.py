import os


APP_NAME = "MyHomeSmart"
APP_VERSION = "2.0α"

CWD = os.getcwd()
APPFOLDER = "MyHomeSmart-HASS-AppDeamon"

APPDEAMONDOCKER_APPS = "/conf/apps"

NEWDB_Sql_path = os.path.join(
    CWD, APPDEAMONDOCKER_APPS, APPFOLDER, "sqlite")
DBPath = os.path.join(
    CWD, APPDEAMONDOCKER_APPS, APPFOLDER, "db")

DB_HistoryName = "history"
DB_CauseEffectName = "causeeffect"

DB_History = os.path.join(DBPath, "%s.db" % (DB_HistoryName))
DB_CauseEffect = os.path.join(DBPath, "%s.db" % (DB_CauseEffectName))

DEBUG_DB = False
