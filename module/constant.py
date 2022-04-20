import os


APP_NAME = "MyHomeSmart"
APP_VERSION = "2.0α"

CWD = os.getcwd()
APPFOLDER = "MyHomeSmart-HASS-AppDeamon"


NEWDB_Sql_path = os.path.join(
    CWD, "/conf/apps", APPFOLDER, "sqlite")
DBPath = os.path.join(APPFOLDER, "db")

DBPath_HistoryName = "history"
DBPath_CauseEffectName = "causeeffect"

DBPath_History = os.path.join(
    CWD, "/conf/apps", DBPath, "%s.db" % (DBPath_HistoryName))
DBPath_CauseEffect = os.path.join(
    CWD, "/conf/apps", DBPath, "%s.db" % (DBPath_CauseEffectName))
