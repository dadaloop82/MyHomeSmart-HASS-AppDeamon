def getConfigValue(self: any, key: str) -> str:
    """_summary_

    Args:
        self (any):       The appDeamon HASS Api
        key (str):        The key to check to return the value

    Returns:
        (str):            The value from key in appDeamon Config
    """
    _config = self.args['config']
    if not key in _config:
        return False
    return _config[key]
