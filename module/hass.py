# Constants
import module.constant as CONSTANT
# Utility
import module.utility as UTILITY


def get_HASSEntities(self: any, includeEntities: dict, excludeEntities: dict) -> dict:
    """Retrieve available entities for myHomeSmart considering those to include and those to exclude

    Args:
        self (any):                 The appDeamon HASS Api
        includeEntities (dict):     The entities to be included in list
        excludeEntities (dict):     The entities to be exclude in list

    Returns:
        dict:                       The entities available to myHomeSmart
    """
    _tmpEntities = {}
    for _entity in includeEntities:
        if "*" in _entity:
            _wEntities = self.get_state(_entity.replace(".*", ""))
            _tmpEntities.update(_wEntities)
        else:
            _sEntity = self.get_state(_entity)
            _tmpEntities.update(_sEntity)
    for _entity in excludeEntities:
        if _entity in _tmpEntities:
            _tmpEntities.pop(_entity)
    return _tmpEntities


def saveEntityDB(self: any,  DB: classmethod, data: dict):
    """save, update or ignore entity on DB

    Args:
        self (any):                 The appDeamon HASS Api
        DB (classmethod):           DATABASE class Method
        data (dict):                The dictionary to save
    """
    query = "INSERT OR IGNORE INTO entity ({k}) VALUES ({v});"
    DB.query(
        self,
        query,
        CONSTANT.DBPath_HistoryName,
        False,
        k=','.join(data.keys()),
        v=UTILITY.parseDictValueForSqlite(data)
    )


def entityUpdate(self: any, DB: classmethod, entityName: str,  newState: str, oldState: str, attrs: dict, editable: bool, kwargs: dict):
    """Manage entity state changes

    Args:
        self (any):                 The appDeamon HASS Api
        DB (module):                DATABASE class Method
        entityName (str):           The name of entity
        attrs (dict):               The attributes of entity
        newState (str):             The current state of entity
        oldState (str):             The old state of entity
        editable (bool):            Entity is of editable or read-only type
        kwargs (dict):              Extra arguments
    """
    friendly_name = kwargs["attrs"]["friendly_name"] if "friendly_name" in kwargs["attrs"] else entityName
    saveEntityDB(
        self, DB, {
            "HASS_Name": entityName,
            "friendly_name": friendly_name,
            "attributes": kwargs["attrs"],
            "editable":  1 if "editable" in kwargs["attrs"] else 0,
            "hash":  hash(entityName)+hash(friendly_name)+hash(editable),
        })
