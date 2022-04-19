def get_HASSEntities(_self, includeEntities, excludeEntities):
    _tmpEntities = {}
    for _entity in includeEntities:
        if "*" in _entity:
            _wEntities = _self.get_state(_entity.replace(".*", ""))
            _tmpEntities.update(_wEntities)
        else:
            _sEntity = _self.get_state(_entity)
            _tmpEntities.update(_sEntity)
    for _entity in excludeEntities:
        if _entity in _tmpEntities:
            _tmpEntities.pop(_entity)
    return _tmpEntities


def update_EditableEntity(_self, entityName, newState, oldState, kwargs):
    _self.log("EditableEntity: %s -> %s" % (entityName, newState))


def update_ReadOnlyEntity(_self, entityName, newState, oldState, kwargs):
    _self.log("ReadOnlyEntity: %s -> %s" % (entityName, newState))
