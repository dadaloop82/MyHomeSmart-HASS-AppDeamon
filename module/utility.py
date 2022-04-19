def getConfigValue(_self, key):
    _config = _self.args['config']
    if not key in _config:
        return False
    return _config[key]



