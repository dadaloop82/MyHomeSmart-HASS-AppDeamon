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

DBPath_HistoryName = "history"
DBPath_CauseEffectName = "causeeffect"

DBPath_History = os.path.join(DBPath, "%s.db" % (DBPath_HistoryName))
DBPath_CauseEffect = os.path.join(DBPath, "%s.db" % (DBPath_CauseEffectName))
