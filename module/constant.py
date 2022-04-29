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

DB_EntityStateName = "entitystate_DB.db"
DB_CauseEffectName = "causeeffect_DB.db"

DB_EntityState = os.path.join(DBPath, "%s" % (DB_EntityStateName))
DB_CauseEffect = os.path.join(DBPath, "%s" % (DB_CauseEffectName))

DEBUG_DB = True
