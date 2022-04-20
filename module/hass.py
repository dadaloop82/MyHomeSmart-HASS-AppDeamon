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


def entityUpdate(self: any, entityName: str, attrs: dict, newState: str, oldState: str, kwargs: dict, editable: bool):
    """Manage entity state changes

    Args:
        self (any):                 The appDeamon HASS Api
        entityName (str):           The name of entity
        attrs (dict):               The attributes of entity
        newState (str):             The current state of entity
        oldState (str):             The old state of entity        
        editable (bool):            Entity is of editable or read-only type
        kwargs (dict):              Extra arguments
    """

    self.log("EditableEntity: %s -> %s" % (entityName, newState))
