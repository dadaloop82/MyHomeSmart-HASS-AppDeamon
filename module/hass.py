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


def saveEntityDB(self: any,  DB: classmethod, data: dict) -> int:
    """save, update or ignore entity on DB

    Args:
        self (any):                 The appDeamon HASS Api
        DB (classmethod):           DATABASE class Method
        data (dict):                The dictionary to save

    Returns:
        (int):                      ID of this entity
    """
    _query = "INSERT OR IGNORE INTO entity ({k}) VALUES ({v});"
    _qS = "SELECT ID FROM entity WHERE HASS_name='%s'" % (data["HASS_Name"])
    return DB.query(
        self,
        _query,
        CONSTANT.DB_EntityState,
        False,
        k=','.join(data.keys()),
        v=UTILITY.parseDictValueForSqlite(data),
        selectQuery=_qS
    )


def saveState(self: any,  DB: classmethod, data: dict, **kwargs: dict) -> int:
    """save, update or ignore entity status on DB

    Args:
        self (any):                 The appDeamon HASS Api
        DB (classmethod):           DATABASE class Method
        data (dict):                The dictionary to save

    Returns:
        (int):                      ID of this entity
    """
    _query = "INSERT OR IGNORE INTO state ({k}) VALUES ({v});"
    _qS = "SELECT ID FROM state WHERE value='{v}' and entityID={e}"
    _qU = "UPDATE state SET frequency=frequency+1 WHERE ID = {id}"
    if kwargs['type'] == "int":
        """ Search for a numerical group that contains it """
        _stateContainGroupID, _qMax = SearchNumericGroupInState(
            self, DB, kwargs['entityID'], float(kwargs["value"]))
        if not _stateContainGroupID:
            data["numvalue_min"] = data["numvalue_max"] = data["value"]
        elif not _qMax:
            return _stateContainGroupID
        else:
            data["numvalue_max"] = _qMax
            data["numvalue_min"] = kwargs["value"]
    return DB.query(
        self,
        _query,
        CONSTANT.DB_EntityState,
        False,
        k=','.join(data.keys()),
        v=UTILITY.parseDictValueForSqlite(data),
        selectQuery=_qS.format(v=kwargs["value"], e=kwargs['entityID']),
        updateQuery=_qU
    )


def saveEntityState(self: any,  DB: classmethod, data: dict, **kwargs: dict) -> int:
    _query = "INSERT OR IGNORE INTO entitystate ({k}) VALUES ({v});"
    return DB.query(
        self,
        _query,
        CONSTANT.DB_EntityState,
        False,
        k=','.join(data.keys()),
        v=UTILITY.parseDictValueForSqlite(data)
    )


def SearchNumericGroupInState(self: any,  DB: classmethod, entityID: int, intValueState: float):
    if not entityID or not intValueState:
        return None, None

    _stateID = 0
    _baseQ = "SELECT state.ID, state.numvalue_min, state.numvalue_max FROM state "
    _baseQ += "INNER JOIN entitystate on entitystate.stateID = state.ID "
    _baseQ += "AND entitystate.entityID = state.entityID "
    _baseQ += "WHERE entitystate.entityID = {e} "

    _q = _baseQ
    _q += "AND {v} BETWEEN state.numvalue_min AND state.numvalue_max"
    _rQ = DB.query(self, _q.format(
        e=entityID, v=intValueState), CONSTANT.DB_EntityState, True)
    if not _rQ:
        """ not cointain - check the best min closest number """
        _q = _baseQ
        _q += "AND state.numvalue_min <= {v} "
        _q += "ORDER BY ABS({v} - state.numvalue_min) "
        _q += "LIMIT 1"
        _rQ = DB.query(self, _q.format(
            e=entityID, v=intValueState), CONSTANT.DB_EntityState, True)
        if _rQ:
            """ best min closest number found """
            """ change the numvalue_max with this current """
            _q = "UPDATE state SET numvalue_max = {v}, value = {v}, frequency=frequency+1 WHERE ID = {id}"
            _stateID = _rQ[0]
            _ = DB.query(self, _q.format(
                v=intValueState, id=_rQ[0]), CONSTANT.DB_EntityState, True)
            return _rQ[0], None
        else:
            """ best min closest number not found """
            """ sarch best max closest number """
            _q = _baseQ
            _q += "AND state.numvalue_max >= {v} "
            _q += "ORDER BY ABS({v} - state.numvalue_max) "
            _q += "LIMIT 1"
            _rQ = DB.query(self, _q.format(
                e=entityID, v=intValueState), CONSTANT.DB_EntityState, True)
            if _rQ:
                """ best max closest number found """
                """ change the numvalue_min with this current """
                _q = "UPDATE state SET numvalue_min = {v}, value = {v}, frequency=frequency+1 WHERE ID = {id}"
                _ = DB.query(self, _q.format(
                    v=intValueState, id=_rQ[0]), CONSTANT.DB_EntityState, True)
                return _rQ[0], None
    else:
        """ is contained """
        _stateID = _rQ[0]
        """ change the numvalue_max with this current """
        _q = "UPDATE state SET numvalue_max = {v} WHERE ID = {id}"
        _ = DB.query(self, _q.format(
            v=intValueState, id=_rQ[0]), CONSTANT.DB_EntityState, True)
        """ create new group with this current value """
        return (_stateID, _rQ[2])
    return (_stateID, None)


def entityUpdate(self: any, DB: classmethod, entityName: str,  newState: str, oldState: str, attrs: dict, editable: bool, lastNodeID: int, lastEditableEntity: int, kwargs: dict) -> tuple:
    friendly_name = kwargs["attrs"]["friendly_name"] if "friendly_name" in kwargs["attrs"] else entityName

    """ Save, update or ignore entity """
    _isEntityEditable = 1 if "editable" in kwargs["attrs"] else 0
    _entityID = saveEntityDB(
        self, DB, {
            "HASS_Name": entityName,
            "friendly_name": friendly_name,
            "attributes": kwargs["attrs"],
            "editable":  _isEntityEditable
        })

    """ Save, update or ignore state """
    _type = "int" if UTILITY.is_number_tryexcept(newState) else "str"
    _stateID = saveState(
        self, DB, {
            "value": newState,
            "entityID": _entityID,
            "type": _type
        },
        value=newState,
        entityID=_entityID,
        type=_type,

    )

    """ Save the entityState """
    _entityStateID = _entityID, saveEntityState(
        self, DB, {
            "entityID": _entityID,
            "stateID": _stateID
        })

    return _entityStateID
