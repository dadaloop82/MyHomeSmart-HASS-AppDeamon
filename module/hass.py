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


def saveEntityDB(self: any,  DB: classmethod, data: dict, hash: hash) -> int:
    """save, update or ignore entity on DB

    Args:
        self (any):                 The appDeamon HASS Api
        DB (classmethod):           DATABASE class Method
        data (dict):                The dictionary to save

    Returns:
        (int):                      ID of this entity
    """
    _query = "INSERT OR IGNORE INTO entity ({k}) VALUES ({v});"
    _qS = "SELECT ID FROM entity WHERE hash='%s'" % (hash)
    return (
        DB.query(
            self,
            _query,
            CONSTANT.DBPath_HistoryName,
            False,
            k=','.join(data.keys()),
            v=UTILITY.parseDictValueForSqlite(data),
            selectQuery=_qS
        ))


def saveEntityStateDB(self: any,  DB: classmethod, data: dict) -> int:
    """save, update or ignore entity status on DB

    Args:
        self (any):                 The appDeamon HASS Api
        DB (classmethod):           DATABASE class Method
        data (dict):                The dictionary to save

    Returns:
        (int):                      ID of this entity
    """
    _query = "INSERT OR IGNORE INTO state ({k}) VALUES ({v});"
    return (
        DB.query(
            self,
            _query,
            CONSTANT.DBPath_HistoryName,
            False,
            k=','.join(data.keys()),
            v=UTILITY.parseDictValueForSqlite(data)
        ))


def saveNodes(self: any,  DB: classmethod, data: dict) -> int:
    _query = "INSERT OR IGNORE INTO nodes ({k}) VALUES ({v});"
    return (
        DB.query(
            self,
            _query,
            CONSTANT.DBPath_HistoryName,
            False,
            k=','.join(data.keys()),
            v=UTILITY.parseDictValueForSqlite(data)
        ))


def entityUpdate(self: any, DB: classmethod, entityName: str,  newState: str, oldState: str, attrs: dict, editable: bool, lastNodeID: int, lastEditableEntity: int, kwargs: dict) -> tuple:

    friendly_name = kwargs["attrs"]["friendly_name"] if "friendly_name" in kwargs["attrs"] else entityName

    """ Save, update or ignore entity """
    _isEntityEditable = 1 if "editable" in kwargs["attrs"] else 0
    _hash = hash(entityName+friendly_name+"E" if editable else "R")
    _entityID = saveEntityDB(
        self, DB, {
            "HASS_Name": entityName,
            "friendly_name": friendly_name,
            "attributes": kwargs["attrs"],
            "editable":  _isEntityEditable,
            "hash":  _hash
        }, _hash)

    """ Save, update or ignore state """
    _stateID = saveEntityStateDB(
        self, DB, {
            "state": newState,
            "type": "int" if UTILITY.is_number_tryexcept(newState) else "str"
        })

    """ Save the nodes when last_entityChanged is not null """
    return _entityID, saveNodes(
        self, DB, {
            "lastEditableEntityID": lastEditableEntity,
            "prevNodeID": lastNodeID,
            "entityID": _entityID,
            "stateID": _stateID,
            "weight": 0
        })
